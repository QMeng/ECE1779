from app.forms import *
from app.models import *
from app.utilities import *
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
    user = load_user(request.cookies.get('userId'))
    user_id = request.cookies.get('userId')
    createTransformationFolder()
    if not os.path.isdir(THUMBNAIL_FOLDER + user_id):
        return render_template('homePage.html', username=user.username)
    else:
        image_names = os.listdir(THUMBNAIL_FOLDER + user_id)#thumbnail的名字
        full_image_names = os.listdir(IMAGE_FOLDER + user_id)
        all_transthumb_names = os.listdir(TRANS_THUMB_FOLDER + user_id)#仅仅是母文件夹
        all_trans_names = os.listdir(TRANSFORM_FOLDER + user_id)
        return render_template('homePage.html', image_names=image_names, username=user.username, full_image_names=full_image_names, all_transthumb_names=all_transthumb_names, all_trans_names=all_trans_names)


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
        return "User not authenticated"

    createImageFolder()
    createThumbnailFolder()
    for image in files:
        user_id = request.cookies.get('userId')
        fileName = image.filename
        destination = "/".join([IMAGE_FOLDER + user_id, fileName])
        image.save(destination)
        thumbnailDestination = create_thumbnail(fileName)
        newImage = ImageContents(user_id=user.get_id(), name=fileName, path=destination, thumbnail_path=thumbnailDestination)
        db.session.add(newImage)
        db.session.commit()

    return "Success"



@app.route("/upload", methods=["POST"])
def upload():
    '''
    This is the upload page. User can upload images.
    '''
    createImageFolder()
    createThumbnailFolder()
    createTransformationFolder()
    createTransThumbnailFolder()
    for upload in request.files.getlist("file"):
        user_id = request.cookies.get('userId')
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
    # check uploading duplications.
        images = os.listdir(IMAGE_FOLDER + user_id)
        for item in images:
            if item == os.path.basename(upload.filename):
                return render_template("error_page.html")
    # save uploading files
        print ("Accept incoming file:", filename)
        target = os.path.join(ROOT, 'images' + user_id)
        destination = "/".join([target, filename])
        upload.save(destination)
    # create 2 transformation images in tranform folder, with a full-size image
        create_transform1(filename)
        create_transform2(filename)
        # create full-size image need to be done
    # Create thumbanils related to uploaded image.
        create_thumbnail(filename)
        thumbnailDestination = create_thumbnail(filename)
        new_image = ImageContents(user_id=user_id, name=filename, path=IMAGE_FOLDER + user_id + filename, thumbnail_path=thumbnailDestination)
        db.session.add(new_image)
        db.session.commit()
    # Create two transformed images related to uploaded image.
        trans1_filename = "trans1" + filename
        trans2_filename = "trans2" + filename
        #print('this is the trans1 filename: {}'.format(trans1_filename))
        #print('this is the trans2 filename: {}'.format(trans2_filename))
        createPictureTransThumbFolder(filename)
        create_trans_thumbnail(trans1_filename, filename)
        create_trans_thumbnail(trans2_filename, filename)
        return render_template("complete_display_image.html", image_name=filename)


@app.route('/upload/<filename>')
def send_image(filename):
    #file name is the original name, like 0910.jpg
    user_id = request.cookies.get('userId')
    return send_from_directory(THUMBNAIL_FOLDER + user_id, filename)

@app.route('/upload/thumbnail<filename>/full')
def send_full_image(filename):
    #file name is the original name, like 0910.jpg
    user_id = request.cookies.get('userId')
    return send_from_directory(IMAGE_FOLDER + user_id, filename)

@app.route('/upload/<filename>/trans/full')
def send_full_image_trans(filename):
    user_id = request.cookies.get('userId')
    return send_from_directory(TRANSFORM_FOLDER + user_id, filename)

@app.route('/upload/<filename>/trans')
def send_image_trans(filename):
    #filename should be transformed picture's name
    user_id = request.cookies.get('userId')
    without_ext = os.path.splitext(filename)[0]
    pic_name = without_ext[6:]
    return send_from_directory(TRANS_THUMB_FOLDER + user_id + "/" + pic_name, "thumbnail"+filename)



@app.route('/Return/')
def return_home():
    return redirect(url_for('home'))
