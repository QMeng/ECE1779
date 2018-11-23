from app_musicUploader.forms import *

from app_musicUploader.utilities import *
from werkzeug.utils import secure_filename


@app_musicUploader.route('/', methods=['GET', 'POST'])
def index():
    '''want the defualt page to be login page'''
    return redirect(url_for('login'))


@app_musicUploader.route('/login', methods=['GET', 'POST'])
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
        if not checkUserAuth(loginForm.username.data, loginForm.password.data):
            # invalid auth, flash message
            flash('Invalid username or password')
            return redirect(url_for('login'))

        user = UserInfo.get(loginForm.username.data)
        # valid user and valid auth, proceed with logging user in
        response = redirect(url_for('home'))
        response.set_cookie('username', user.username)
        return response

    # if the submitted form is sign up form
    if signupForm.validate_on_submit() and signupForm.submitSignUpInfo.data:
        if not checkUserExists(signupForm.username.data):
            # new user, proceed with register into database
            user = UserInfo(signupForm.username.data)
            user.set_email(signupForm.email.data)
            user.set_password(signupForm.password.data)
            user.save()
            return redirect(url_for('login'))
        else:
            # existing user, flash the message
            flash("User already signed up!")
            return redirect(url_for('signup'))
    return render_template('login.html', title='Sign In', loginForm=loginForm, signupForm=signupForm)


@app_musicUploader.route('/home', methods=['GET', 'POST'])
def home():
    '''
    This is the home page, after user logs in, this page will have option to upload file and displays all the previous
    images uploaded by the user
    :return:
    the rendered page of current user's home
    '''
    form = FileUploadForm()

    user = load_user(request.cookies.get('username'))
    original_thumbnail_images = getUserOriginalImages(user.username)
    all_images = getUserImages(user.username)
    original_thumbnail_url = getPresignedUrl(user.username, original_thumbnail_images, False)
    all_thumbnail_url = getPresignedUrl(user.username, all_images, False)
    all_image_url = getPresignedUrl(user.username, all_images, True)

    if form.validate_on_submit():
        image = form.image.data
        music = form.music.data
        imageName = secure_filename(image.filename)
        musicName = secure_filename(music.filename)
        saveName = computeFileName(imageName, '-1.')
        username = request.cookies.get("username")

        createImageFolder(username)
        createThumbnailFolder(username)

        # check uploading duplications.
        if check_dup(imageName, username):
            flash("file already existed")
            return redirect(url_for('home'))

        # save uploading files
        destination = os.path.join(IMAGE_FOLDER, username, saveName)
        image.save(destination)
        uploadIntoS3(username, destination, saveName, True)

        # create multishift, black and white, sepia transformations
        image_bucket = create_transformations(imageName, username)

        # Create thumbanil related to uploaded image.
        thumbnail_bucket = create_thumbnail(imageName, username)

        # save the image info in DB
        new_image = ImageInfo(username, imageName)
        new_image.set_s3ImageBucket(image_bucket)
        new_image.set_s3ThumbnailBucket(thumbnail_bucket)
        new_image.save()
        wipeOutLocalImage(username)
        return redirect(url_for('home'))
    else:
        flash('File type not supported')

    return render_template('homePage.html', orig_tbn_img=original_thumbnail_images, all_images=all_images,
                           orig_tbn_url=original_thumbnail_url, all_tbn_url=all_thumbnail_url,
                           all_image_url=all_image_url, username=user.username, form=form)


@app_musicUploader.route('/logout')
def logout():
    '''
    this method logs out current user and removes the user's cookie from the brower by setting its expire time to now
    this method also removed local images and thumbnails
    '''
    wipeOutLocalImage(request.cookies.get('username'))
    response = redirect(url_for('login'))
    response.set_cookie('username', '', expires=0)
    return response


@app_musicUploader.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    '''handle the invalid usage of this app_worker.'''
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app_musicUploader.route('/wipeout')
def wipe_out_data():
    '''
    wipe out current user's data
    '''
    username = request.cookies.get("username")
    imageBucket = IMAGE_BUCKET_PREFIX + username
    thumbnailBucket = THUMBNAIL_BUCKET_PREFIX + username

    result = ImageInfo.query(username)
    for item in result:
        image = ImageInfo.get(item.username, item.imagename)
        image.delete()

    if checkBucketExist(imageBucket):
        bucket = s3_resource.Bucket(imageBucket)
        for obj in bucket.objects.all():
            obj.delete()
        bucket.delete()

    if checkBucketExist(thumbnailBucket):
        bucket = s3_resource.Bucket(thumbnailBucket)
        for obj in bucket.objects.all():
            obj.delete()
        bucket.delete()

    return redirect(url_for('home'))
