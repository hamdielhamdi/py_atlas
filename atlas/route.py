from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user,LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

from atlas import app,db
from atlas.form import RegisterForm,LoginForm,QuestionForm
from atlas.model import Question,User


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html', name=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('You were successfully logged in')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid credentials'
        else:
            error = 'Invalid credentials'

    return render_template('login.html', form=form, error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    content = Question.query.filter_by(person_id=current_user.id).all()
    return render_template('dashboard.html', name=current_user.username, content=content)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/askme', methods=['GET', 'POST'])
@login_required
def askme():
    form = QuestionForm()
    if form.validate_on_submit():
        if len(request.files) != 0:
            files = request.files["file"]
        else:
            files = False
        if files:
            file_name = files.filename
            file = files.read()
        else:
            file_name = None
            file = None
        new_question = Question(file=file, file_name=file_name, content=form.content.data,
                                person_id=current_user.id)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('askme.html', form=form, name=current_user.username)



