from app.forms import *
from app.models import *
from flask_login import current_user, login_user, login_required


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login page for user to login.
    :return:
    User home page if user is authenticated. Error messages otherwise
    '''
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=remember)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    '''
    This is the home page, after user logs in, this page will have option to upload file and displays all the previous
    images uploaded by the user
    :return:
    the rendered page of current user's home

    TODO: do it
    '''
    return render_template('homePage.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    '''
    This is the sign up page. User will need to fill the user name, password, email fields in order to sign up.
    Identical usernames will be detected.
    '''
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if (user is None):
            user = User(form.username.data, form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash("User already signed up!")
            return redirect(url_for('signup'))
    return render_template('signUp.html', title='Sign Up', form=form)
