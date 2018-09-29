from app.forms import *
from app.models import *
from app.utility import find_path, create_thumbnail, check_duplication, build_thum_dir
from flask_login import login_user, login_required, logout_user


@app.route('/')
def index():
    '''want the defualt page to be login page'''
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login page for user to login.
    :return:
    User home page if user is authenticated. Error messages otherwise
    '''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        response = redirect(url_for('home'))
        response.set_cookie('userId', user.get_id())
        return response
    return render_template('login.html', title='Sign In', form=form)


@app.route('/home')
@login_required
def home():
    '''
    This is the home page, after user logs in, this page will have option to upload file and displays all the previous
    images uploaded by the user
    :return:
    the rendered page of current user's home

    TODO: do it
    '''
    user = load_user(request.cookies.get('userId'))
    target = os.path.join(APP_ROOT, 'thumbnails_' + request.cookies.get('userId'))
    if not os.path.isdir(target):
         return render_template('homePage.html', username=user.username)
    else:
         image_names = os.listdir(APP_ROOT + '/thumbnails_' + request.cookies.get('userId'))
         print(image_names)
         return render_template('homePage.html', image_names=image_names, username=user.username)


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


@app.route('/logout')
def logout():
    logout_user()
    request.cookies.clear()
    return redirect(url_for('login'))


@app.route("/upload", methods=["POST"])
def upload():
    '''
    This is the upload page. User can upload images.
    '''
    user = request.cookies.get('userId')
    target = os.path.join(APP_ROOT, 'images_' + user)
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):

        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename

    ## check uploading duplications.
        thum_path = build_thum_dir()
        os.chdir(thum_path)
        thum_images = os.listdir(APP_ROOT + '/images_' + request.cookies.get('userId'))
        for name in thum_images:
            if name == os.path.basename(upload.filename):
                return render_template("error_page.html")
    ## save uploading files
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)

        os.chdir(target)
        t_path = find_path()
        create_thumbnail(filename, 200, 200)

        new_image = ImageContents(user_id=user, name=filename, path=destination, thumbnail_path=t_path)
        db.session.add(new_image)
        db.session.commit()

        return render_template("complete_display_image.html", image_name=filename)


@app.route('/upload/<filename>')
def send_image(filename):
    user = request.cookies.get('userId')
    return send_from_directory("thumbnails_" + user, filename)


@app.route('/Return/')
def return_home():
    return redirect(url_for('home'))