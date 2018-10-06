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
    '''
    form = FileForm()
    user = load_user(request.cookies.get('userId'))
    user_id = request.cookies.get('userId')
    if not os.path.isdir(os.path.join(THUMBNAIL_FOLDER, user_id)):
        return render_template('homePage.html', username=user.username, form=form)
    else:
        image_names = glob.glob1(os.path.join(THUMBNAIL_FOLDER, user_id), "*-1*")
        return render_template('homePage.html', image_names=image_names, username=user.username, form=form)


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
        fileName = image.filename

        if (check_dup(fileName, user.get_id())):
            error = InvalidUsage("The image you tried to upload already exists. Please try another file")
            return handle_invalid_usage(error)

        destination = os.path.join(IMAGE_FOLDER, user.get_id(), fileName)
        image.save(destination)
        thumbnailDestination = create_thumbnail(fileName, user.get_id())
        newImage = ImageContents(user_id=user.get_id(), name=fileName, path=destination,
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
    if form.validate_on_submit():
        f = form.file.data
        #将filename变为了nameAndType
        nameAndType = secure_filename(f.filename)#0910-4.png
        nameAndTypeList = nameAndType.split('.')#[0910-4, .png]
        fileName = "".join(nameAndTypeList[:-1])
        fileType = nameAndTypeList[-1]
        saveName = fileName + '-1.' + fileType
        #filename = secure_filename(f.filename)
        user_id = request.cookies.get("userId")

        createImageFolder(user_id)
        createThumbnailFolder(user_id)

        # check uploading duplications.
        if check_dup(saveName, user_id):
            return render_template("error_page.html")

        # save uploading files

        destination = os.path.join(IMAGE_FOLDER, user_id, saveName)
        f.save(destination)

        # Create thumbanil related to uploaded image.
        thumbnailDestination = create_thumbnail(saveName, user_id)

        # Create transformation related to uploaded image.
        levelDestination = create_level(nameAndType, user_id)
        leftshiftDestination = create_leftshift(nameAndType, user_id)
        #暂时不动数据库

        # save the image info in DB
        new_image = ImageContents(user_id=user_id, name=nameAndType, path=destination, thumbnail_path=thumbnailDestination)#不确定是否为saveName
        db.session.add(new_image)
        db.session.commit()
        return render_template("complete_display_image.html", image_name=nameAndType)

    else:
        user = load_user(request.cookies.get('userId'))
        user_id = request.cookies.get('userId')
        image_names = glob.glob1(os.path.join(THUMBNAIL_FOLDER, user_id), "*-1*")#不确定
        return render_template('homePage.html', image_names=image_names, username=user.username, form=form)


@app.route('/upload/<filename>')
def send_thumbnail(filename):
    '''send the thumbnail image to the web page'''
    user_id = request.cookies.get('userId')
    return send_from_directory(os.path.join(THUMBNAIL_FOLDER, user_id), filename)

@app.route('/upload/<filename>/full')
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
