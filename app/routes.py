from app.forms import *
from app.models import *
from app.utilities import *
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename
import glob


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
    loginForm = LoginForm()
    signupForm = SignUpForm()
    if loginForm.validate_on_submit() and loginForm.submitLoginInfo.data:
        user = User.query.filter_by(username=loginForm.username.data).first()
        if user is None or not user.check_password(loginForm.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=loginForm.remember_me.data)
        response = redirect(url_for('home'))
        response.set_cookie('userId', user.get_id())
        return response
    if signupForm.validate_on_submit() and signupForm.submitSignUpInfo.data:
        user = User.query.filter_by(username=signupForm.username.data).first()
        if (user is None):
            user = User(signupForm.username.data, signupForm.email.data)
            user.set_password(signupForm.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash("User already signed up!")
            return redirect(url_for('signup'))
    return render_template('login.html', title='Sign In', loginForm=loginForm, signupForm=signupForm)



@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    '''
    This is the home page, after user logs in, this page will have option to upload file and displays all the previous
    images uploaded by the user
    :return:
    the rendered page of current user's home
    '''
    form = FileForm()
    user = load_user(request.cookies.get('userId'))
    if not os.path.isdir(os.path.join(THUMBNAIL_FOLDER, user.get_id())):
        return render_template('homePage.html', username=user.username, form=form)
    else:
        image_names = glob.glob1(os.path.join(THUMBNAIL_FOLDER, user.get_id()), "*-1.*")
        return render_template('homePage.html', image_names=image_names, username=user.username, form=form)

@app.route('/logout')
def logout():
    '''this method logs out current user and removes the user's cookie from the brower by setting its expire time to now
    '''
    logout_user()
    response = redirect(url_for('login'))
    response.set_cookie('userId', '', expires=0)
    return response


@app.route('/test/FileUpload', methods=['POST'])
def testFileUpload():
    '''/test/FileUpload uri endpoint for easy uploading thru api calls'''
    username = request.form['userID']
    password = request.form['password']
    files = request.files.getlist('uploadedFile')

    user = User.query.filter_by(username=username).first()
    if (not user.check_password(password)):
        error = InvalidUsage("User not authenticated")
        return handle_invalid_usage(error)

    createImageFolder(user.get_id())
    createThumbnailFolder(user.get_id())

    for image in files:
        imageName = image.filename
        saveName = computeFileName(imageName, '-1.')
        if (check_dup(imageName, user.get_id())):
            error = InvalidUsage("The image you tried to upload already exists. Please try another file")
            return handle_invalid_usage(error)

        destination = os.path.join(IMAGE_FOLDER, user.get_id(), saveName)
        image.save(destination)

        create_transformations(imageName, user.get_id())
        thumbnailDestination = create_thumbnail(imageName, user.get_id())
        newImage = ImageContents(user_id=user.get_id(), name=imageName, path=os.path.join(IMAGE_FOLDER, user.get_id()),
                                 thumbnail_path=thumbnailDestination)
        db.session.add(newImage)
        db.session.commit()

    return "Success"


@app.route("/upload", methods=["POST"])
def upload():
    '''
    This is the upload page. User can upload images.
    '''
    form = FileForm()
    upload_failure = '1 upload failed: '
    if form.validate_on_submit():
        f = form.file.data
        imageName = secure_filename(f.filename)
        saveName = computeFileName(imageName, '-1.')
        user_id = request.cookies.get("userId")

        createImageFolder(user_id)
        createThumbnailFolder(user_id)

        # check uploading duplications.
        if check_dup(imageName, user_id):
            user = load_user(request.cookies.get('userId'))
            image_names = glob.glob1(os.path.join(THUMBNAIL_FOLDER, user.get_id()), "*-1.*")
            duplicate_err = 'file already existed'
            return render_template('homePage.html', image_names=image_names, username=user.username, form=form, check=duplicate_err)

        # save uploading files
        destination = os.path.join(IMAGE_FOLDER, user_id, saveName)
        f.save(destination)

        # create multishift, black and white, sepia transformations
        create_transformations(imageName, user_id)

        # Create thumbanil related to uploaded image.
        thumbnailDestination = create_thumbnail(imageName, user_id)

        # save the image info in DB
        new_image = ImageContents(user_id=user_id, name=imageName, path=os.path.join(IMAGE_FOLDER, user_id),
                                  thumbnail_path=thumbnailDestination)
        db.session.add(new_image)
        db.session.commit()
        user = load_user(request.cookies.get('userId'))
        image_names = glob.glob1(os.path.join(THUMBNAIL_FOLDER, user.get_id()), "*-1.*")
        return render_template('homePage.html', image_names=image_names, username=user.username, form=form)

    else:
        print('here')
        format_err = upload_failure + 'file type unsupported'
        user = load_user(request.cookies.get('userId'))
        image_names = glob.glob1(os.path.join(THUMBNAIL_FOLDER, user.get_id()), "*-1.*")
        return render_template('homePage.html', image_names=image_names, username=user.username, form=form, check=format_err)


@app.route('/upload/<filename>')
def send_thumbnail(filename):
    '''send the thumbnail image to the web page'''
    user_id = request.cookies.get('userId')
    return send_from_directory(os.path.join(THUMBNAIL_FOLDER, user_id), filename)


@app.route('/upload/thumbnail_<filename>/full')
def send_full(filename):
    '''send the full-size image to the web page'''
    user_id = request.cookies.get('userId')
    return send_from_directory(os.path.join(IMAGE_FOLDER, user_id), filename)


@app.route('/Return/')
def return_home():
    return redirect(url_for('home'))


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    '''handle the invalid usage of this app.'''
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(ROOT, 'app', 'static'), 'background-home02.jpeg')
