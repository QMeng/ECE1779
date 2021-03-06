from app_musicUploader.forms import *

from app_musicUploader.utilities import *
from werkzeug.utils import secure_filename
from tinytag import *
import datetime


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
            flash('Invalid username or password', category='loginError')
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
            user.set_email(signupForm.email.data).set_password(signupForm.password.data).set_share(False).save()
            return redirect(url_for('login'))
        else:
            # existing user, flash the message
            flash("User already signed up!", category='loginError')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', loginForm=loginForm, signupForm=signupForm)


@app_musicUploader.route('/home', methods=['GET', 'POST'])
def home():
    '''
    This is the home page, after user logs in, this page will have option to upload file and displays all the previous
    images uploaded by the user
    :return:
    the rendered page of current user's home
    '''
    fileform = FileUploadForm()

    user = load_user(request.cookies.get('username'))
    images = getUserImages(user.username, 1)
    musics = getUserMusics(user.username, 1)
    durations = getMusicDurations(user.username, 1)
    artists = getMusicArtists(user.username, 1)
    thumbnail_urls = getPresignedUrl(user.username, images, 2)
    image_urls = getPresignedUrl(user.username, images, 1)
    music_urls = getPresignedUrl(user.username, musics, 3)

    if fileform.validate_on_submit():
        image = fileform.image.data
        music = fileform.music.data
        imagename = secure_filename(image.filename).replace(" ", "_")
        musicname = secure_filename(music.filename)
        username = request.cookies.get("username")

        createImageFolder(username)
        createThumbnailFolder(username)
        createMusicFolder(username)

        # check uploading duplications.
        if check_dup(musicname, username):
            flash("file already existed", "uploadError")
            return redirect(url_for('home'))

        # save uploading files
        image_des = os.path.join(IMAGE_FOLDER, username, imagename)
        image.save(image_des)
        image_bucket = uploadIntoS3(username, image_des, imagename, 1)

        music_des = os.path.join(MUSIC_FOLDER, username, musicname)
        music.save(music_des)
        music_bucket = uploadIntoS3(username, music_des, musicname, 3)

        tag = TinyTag.get(music_des)
        seconds = int(tag.duration)
        second = int(seconds % 60)
        if second < 10:
            second = "0" + str(second)
        else:
            second = str(second)

        minSec = str(int(seconds / 60)) + ":" + second
        artist = tag.artist
        if artist == None:
            artist = "None"

        # Create thumbanil related to uploaded image.
        thumbnail_bucket = create_thumbnail(imagename, username)

        # save the music info in DB
        music = MusicInfo(username)
        music.set_musicname(musicname).set_duration(minSec).set_artist(artist).set_imagename(
            imagename).set_s3MusicBucket(music_bucket).set_s3ImageBucket(image_bucket).set_s3ThumbnailBucket(
            thumbnail_bucket).save()

        wipeOutContent(username)
        return redirect(url_for('home'))
    else:
        flash("Please upload files with correct type", category='uploadError')

    return render_template('homePage.html', username=user.username, form=fileform, thumbnail_urls=thumbnail_urls,
                           image_urls=image_urls, music_urls=music_urls, durations=durations, artists=artists,
                           images=images, musics=musics)


@app_musicUploader.route('/playlist')
def playlist():
    '''
    renders the playlist page
    '''
    user = load_user(request.cookies.get("username"))
    images = getUserImages(user.username, 2)
    musics = getUserMusics(user.username, 2)
    durations = getMusicDurations(user.username, 2)
    artists = getMusicArtists(user.username, 2)
    thumbnail_urls = getPresignedUrl(user.username, images, 2)
    image_urls = getPresignedUrl(user.username, images, 1)
    music_urls = getPresignedUrl(user.username, musics, 3)

    return render_template('playlist.html', images=images, musics=musics, durations=durations, artists=artists,
                           thumbnail_urls=thumbnail_urls, image_urls=image_urls, music_urls=music_urls)


@app_musicUploader.route('/guestplaylist/<username>')
def displayGuestPlaylist(username):
    username = decode(Config.SECRET_KEY, username)
    user = load_user(username)

    if not user.share:
        return render_template("playlistNotAvailable.html")

    images = getUserImages(username, 2)
    musics = getUserMusics(username, 2)
    durations = getMusicDurations(username, 2)
    artists = getMusicArtists(username, 2)
    thumbnail_urls = getPresignedUrl(username, images, 2)
    image_urls = getPresignedUrl(username, images, 1)
    music_urls = getPresignedUrl(username, musics, 3)

    return render_template('guestPlaylist.html', images=images, musics=musics, durations=durations, artists=artists,
                           thumbnail_urls=thumbnail_urls, image_urls=image_urls, music_urls=music_urls)


@app_musicUploader.route('/cleanList')
def cleanList():
    '''
    delete all things in the play list, jump back to home pages
    '''
    user = load_user(request.cookies.get("username"))
    result = MusicList.query(user.username)
    for item in result:
        music = MusicList.get(item.username, item.musicname)
        music.delete()
    return redirect(url_for('home'))


@app_musicUploader.route('/logout')
def logout():
    '''
    this method logs out current user and removes the user's cookie from the brower by setting its expire time to now
    this method also removed local images and thumbnails
    '''
    wipeOutContent(request.cookies.get('username'))
    response = redirect(url_for('login'))
    response.set_cookie('username', '', expires=0)
    return response


@app_musicUploader.route('/wipeout')
def wipe_out_data():
    '''
    wipe out current user's data
    '''
    username = request.cookies.get("username")
    imageBucket = IMAGE_BUCKET_PREFIX + username
    thumbnailBucket = THUMBNAIL_BUCKET_PREFIX + username
    musicBucket = MUSIC_BUCKET_PREFIX + username

    result = MusicInfo.query(username)
    for item in result:
        music = MusicInfo.get(item.username, item.musicname)
        music.delete()

    result = MusicList.query(username)
    for item in result:
        listItem = MusicList.get(item.username, item.musicname)
        listItem.delete()

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

    if checkBucketExist(musicBucket):
        bucket = s3_resource.Bucket(musicBucket)
        for obj in bucket.objects.all():
            obj.delete()
        bucket.delete()

    return redirect(url_for('home'))


@app_musicUploader.route('/addToList', methods=['Get', 'POST'])
def addToList():
    '''
    add the music into play list
    '''
    user = load_user(request.cookies.get("username"))
    musicname = request.args.get('jsdata')
    item = MusicList(user.username)
    musicInfo = MusicInfo.get(user.username, musicname)
    item.set_musicname(musicname).set_duration(musicInfo.duration).set_artist(musicInfo.artist).set_imagename(
        musicInfo.imagename).save()
    return ""


@app_musicUploader.route('/removeFromList/<musicname>', methods=['Get', 'Post'])
def removeFromList(musicname):
    '''
    remove the music from play list
    '''
    user = load_user(request.cookies.get("username"))
    if MusicList.count(user.username, MusicList.musicname == musicname) != 0:
        tobeDeleted = MusicList.get(user.username, musicname)
        tobeDeleted.delete()
    return redirect(url_for('playlist'))


@app_musicUploader.route('/sharePlaylist', methods=['Get', 'Post'])
def sharePlaylist():
    '''
    share the play list
    '''
    user = load_user(request.cookies.get("username"))
    user.set_share(True).save()
    url = "https://musicuploader.damonqingsongmeng.com/guestplaylist/" + encode(Config.SECRET_KEY, user.username)
    return render_template('shareLink.html', link=url)


@app_musicUploader.route('/stopSharing', methods=['Get', 'Post'])
def stopSharing():
    '''
    stop sharing the playlist
    '''
    user = load_user(request.cookies.get("username"))
    user.set_share(False).save()
    return ""


@app_musicUploader.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    '''handle the invalid usage of this app_worker.'''
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
