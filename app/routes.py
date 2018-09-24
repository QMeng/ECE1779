from flask import *
from werkzeug.security import generate_password_hash

from app import *
from app.forms import *


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login page for user to login.
    :return:
    User home page if user is authenticated. Error messages otherwise

    TODO: need to work on the auth part. also, how do we let other page know which user this is? cookies?
    '''
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        global user
        user = {'username': form.username.data}
        return redirect(url_for('homePage'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/home')
def homePage():
    '''
    This is the home page, after user logs in, this page will have option to upload file and displays all the previous
    images uploaded by the user
    :return:
    the rendered page of current user's home

    TODO: do it
    '''
    return render_template('homePage.html', user=user)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    '''
    This is the sign up page. User will need to fill the user name, password, email fields in order to sign up.
    Identical usernames will be detected.

    TODO: add salt for the password. may need to fine-tune the shit a little bit, e.g. confirm password, email input pattern matching
    '''
    form = SignUpForm()
    email = form.email.data
    username = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        conn = mysql.connect()
        cursor = conn.cursor()
        hashedPassword = generate_password_hash(password, method='pbkdf2:sha256:1000')
        cursor.execute("SELECT * FROM UserInfo WHERE user_username = %s", [username])
        result = cursor.fetchall()
        if (len(result) != 0):
            flash("User already exists!")
            return redirect(url_for('signup'))
        else:
            cursor.execute("INSERT INTO UserInfo(user_username, user_email, user_password) VALUES(%s, %s, %s)",
                        (username, email, password))
            conn.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('signUp.html', title='Sign Up', form=form)
