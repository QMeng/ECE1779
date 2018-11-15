from app_worker.forms import *
from app_worker.utilities import *
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename


@app_worker.route('/')
def index():
    '''want the defualt page to be login page'''
    return redirect(url_for('login'))


@app_worker.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login page for user to login.
    :return:
    User home page if user is authenticated. Error messages otherwise
    '''
    loginForm = LoginForm()
    signupForm = SignUpForm()

    # if the submitted form is login form
    if loginForm.validate_on_submit() and loginForm.submitLoginInfo.data:
        user = User.query.filter_by(username=loginForm.username.data).first()
        if user is None or not user.check_password(loginForm.password.data):
            # invalid auth, flash message
            flash('Invalid username or password')
            return redirect(url_for('login'))

        # valid user and valid auth, proceed with logging user in
        login_user(user, remember=loginForm.remember_me.data)
        response = redirect(url_for('home'))
        response.set_cookie('userId', user.get_id())
        return response

    # if the submitted form is sign up form
    if signupForm.validate_on_submit() and signupForm.submitSignUpInfo.data:
        user = User.query.filter_by(username=signupForm.username.data).first()
        if (user is None):
            # new user, proceed with register into database
            user = User(signupForm.username.data, signupForm.email.data)
            user.set_password(signupForm.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            # existing user, flash the message
            flash("User already signed up!")
            return redirect(url_for('signup'))
    return render_template('login.html', title='Sign In', loginForm=loginForm, signupForm=signupForm)


@app_worker.route('/home', methods=['GET', 'POST'])
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
    original_thumbnail_images = getUserOriginalImages(user.get_id())
    all_images = getUserImages(user.get_id())
    original_thumbnail_url = getPresignedUrl(user.get_id(), original_thumbnail_images, False)
    all_thumbnail_url = getPresignedUrl(user.get_id(), all_images, False)
    all_image_url = getPresignedUrl(user.get_id(), all_images, True)
    return render_template('homePage.html', orig_tbn_img=original_thumbnail_images, all_images=all_images,
                           orig_tbn_url=original_thumbnail_url, all_tbn_url=all_thumbnail_url,
                           all_image_url=all_image_url, username=user.username, form=form)


@app_worker.route('/logout')
def logout():
    '''
    this method logs out current user and removes the user's cookie from the brower by setting its expire time to now
    this method also removed local images and thumbnails
    '''
    wipeOutLocalImage(request.cookies.get('userId'))
    logout_user()
    response = redirect(url_for('login'))
    response.set_cookie('userId', '', expires=0)
    return response


@app_worker.route('/test/FileUpload', methods=['POST'])
def testFileUpload():
    '''/test/FileUpload uri endpoint for easy uploading thru api calls'''
    username = request.form['userID']
    password = request.form['password']
    files = request.files.getlist('uploadedfile')

    user = User.query.filter_by(username=username).first()
    if (not user.check_password(password)):
        error = InvalidUsage("User not authenticated")
        return handle_invalid_usage(error)

    createImageFolder(user.get_id())
    createThumbnailFolder(user.get_id())

    # save the uploaded image
    for image in files:
        imageName = image.filename
        saveName = computeFileName(imageName, '-1.')

        # check for duplicate
        if (check_dup(imageName, user.get_id())):
            error = InvalidUsage("The image you tried to upload already exists. Please try another file")
            return handle_invalid_usage(error)

        # save to local, then upload into S3
        destination = os.path.join(IMAGE_FOLDER, user.get_id(), saveName)
        image.save(destination)
        uploadIntoS3(user.get_id(), destination, saveName, True)

        # create transformation and their thumbnails, upload into S3
        create_transformations(imageName, user.get_id())
        thumbnailDestination = create_thumbnail(imageName, user.get_id())
        newImage = ImageContents(user_id=user.get_id(), name=imageName, path=os.path.join(IMAGE_FOLDER, user.get_id()),
                                 thumbnail_path=thumbnailDestination)

        # update DB session
        db.session.add(newImage)
        db.session.commit()
    wipeOutLocalImage(user.get_id())

    return "Success"


@app_worker.route("/upload", methods=["POST"])
def upload():
    '''
    This is the upload page. User can upload images.
    '''
    form = FileForm()
    if form.validate_on_submit():
        f = form.file.data
        imageName = secure_filename(f.filename)
        saveName = computeFileName(imageName, '-1.')
        user_id = request.cookies.get("userId")

        createImageFolder(user_id)
        createThumbnailFolder(user_id)

        # check uploading duplications.
        if check_dup(imageName, user_id):
            flash("file already existed")
            return redirect(url_for('home'))

        # save uploading files
        destination = os.path.join(IMAGE_FOLDER, user_id, saveName)
        f.save(destination)
        uploadIntoS3(user_id, destination, saveName, True)

        # create multishift, black and white, sepia transformations
        create_transformations(imageName, user_id)

        # Create thumbanil related to uploaded image.
        thumbnailDestination = create_thumbnail(imageName, user_id)

        # save the image info in DB
        new_image = ImageContents(user_id=user_id, name=imageName, path=os.path.join(IMAGE_FOLDER, user_id),
                                  thumbnail_path=thumbnailDestination)
        db.session.add(new_image)
        db.session.commit()
        wipeOutLocalImage(user_id)
    else:
        flash('File type not supported')
    return redirect(url_for('home'))


@app_worker.route('/Return/')
def return_home():
    return redirect(url_for('home'))


@app_worker.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    '''handle the invalid usage of this app_worker.'''
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app_worker.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(ROOT, 'app_worker', 'static'), 'background-home02.jpeg')
