from builtins import round

import botocore
from pynamodb.exceptions import DoesNotExist

from app_musicUploader.models import *
from PIL import Image
from resizeimage import resizeimage

import glob


def createImageFolder(username):
    '''
    create folder to store images uploaded by the user
    the location should be [project dir]/images
    '''
    if not os.path.isdir(IMAGE_FOLDER):
        os.mkdir(IMAGE_FOLDER)
    if not os.path.isdir(os.path.join(IMAGE_FOLDER, username)):
        os.mkdir(os.path.join(IMAGE_FOLDER, username))


def createThumbnailFolder(username):
    '''
    create folder to store thumbnails of the images uploaded by the user
    the location should be [project dir]/thumbnails
    '''
    if not os.path.isdir(THUMBNAIL_FOLDER):
        os.mkdir(THUMBNAIL_FOLDER)
    if not os.path.isdir(os.path.join(THUMBNAIL_FOLDER, username)):
        os.mkdir(os.path.join(THUMBNAIL_FOLDER, username))


def createMusicFolder(username):
    '''
    create folder to store music and its transformations
    '''
    if not os.path.isdir(MUSIC_FOLDER):
        os.mkdir(MUSIC_FOLDER)
    if not os.path.isdir(os.path.join(MUSIC_FOLDER, username)):
        os.mkdir(os.path.join(MUSIC_FOLDER, username))


def create_thumbnail(source_file, username):
    '''create thumbnail for the image uploaded by user'''

    # creating, saving and uploadind into S3 for the thumbnail

    with open(os.path.join(IMAGE_FOLDER, username, source_file), 'r+b') as f:
        with Image.open(f) as img:
            new_width = img._size[0] / (img._size[1] / 250)
            img = resizeimage.resize_thumbnail(img, [new_width, 250])
            img.save(os.path.join(THUMBNAIL_FOLDER, username, source_file), img.format)
            uploadIntoS3(username, os.path.join(THUMBNAIL_FOLDER, username, source_file), source_file, 2)
        f.close()

    return THUMBNAIL_BUCKET_PREFIX + username


def check_dup(musicname, username):
    '''
    check to see if there are music belong to the user in database that has the same name
    '''
    music_list = MusicInfo.query(username)
    for music in music_list:
        if music.musicname == musicname:
            return True
    return False


def computeFileName(musicName, trail):
    '''
    this method computes the correct actual file name of the music we are looking for.
    '''
    nameAndType = musicName.split('.')
    fileName = "".join(nameAndType[:-1])
    fileType = nameAndType[-1]
    rcName = fileName + trail + fileType
    return rcName


def uploadIntoS3(username, filePath, fileName, type):
    '''
    Upload image into S3 bucket
    :param username: user id of current user
    :param filePath: path leading to the file that we want to upload
    :param fileName: file name
    :param isImage: set to true if it is image, set to false if it is thumbnail
    '''
    if type == 1:
        bucketName = IMAGE_BUCKET_PREFIX + username
    elif type == 2:
        bucketName = THUMBNAIL_BUCKET_PREFIX + username
    else:
        bucketName = MUSIC_BUCKET_PREFIX + username

    if not checkBucketExist(bucketName):
        s3_resource.create_bucket(Bucket=bucketName)
    s3_resource.Bucket(bucketName).upload_file(Filename=filePath, Key=fileName)

    return bucketName


def checkBucketExist(bucketName):
    '''
    check if specific s3 bucket exists or not
    '''
    try:
        s3_resource.meta.client.head_bucket(Bucket=bucketName)
        return True
    except botocore.exceptions.ClientError as e:
        return False


def wipeOutContent(username):
    '''
    remove all the user's files from local
    '''
    if os.path.isdir(os.path.join(IMAGE_FOLDER, username)):
        files = glob.glob(os.path.join(IMAGE_FOLDER, username, '*'))
        for file in files:
            os.remove(file)
        os.removedirs(os.path.join(IMAGE_FOLDER, username))
    if os.path.isdir(os.path.join(THUMBNAIL_FOLDER, username)):
        files = glob.glob(os.path.join(THUMBNAIL_FOLDER, username, '*'))
        for file in files:
            os.remove(file)
        os.removedirs(os.path.join(THUMBNAIL_FOLDER, username))

    if os.path.isdir(os.path.join(MUSIC_FOLDER, username)):
        files = glob.glob(os.path.join(MUSIC_FOLDER, username, '*'))
        for file in files:
            os.remove(file)
        os.removedirs(os.path.join(MUSIC_FOLDER, username))


def getUserImages(username, type):
    '''
    get the original images belong to this user in the database
    '''
    if type == 1:
        musics = MusicInfo.query(username)
    else:
        musics = MusicList.query(username)

    keys = []
    for music in musics:
        keys.append(music.imagename)

    return keys


def getUserMusics(username, type):
    '''
    get all the musics belong to this user in the database
    '''
    if type == 1:
        musics = MusicInfo.query(username)
    else:
        musics = MusicList.query(username)

    keys = []
    for music in musics:
        keys.append(music.musicname)

    return keys


def getPresignedUrl(username, file_list, type):
    '''
    compute the presigned urls for the files in S3
    '''
    if type == 1:
        bucket = IMAGE_BUCKET_PREFIX + username
    elif type == 2:
        bucket = THUMBNAIL_BUCKET_PREFIX + username
    else:
        bucket = MUSIC_BUCKET_PREFIX + username

    urls = []
    for file in file_list:
        url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': file})
        urls.append(url)
    return urls


def checkUserAuth(username, password):
    '''
    :return: True if the username exists and password is correct
    '''
    try:
        user = UserInfo.get(username)
        if user.check_password(password):
            return True
        return False
    except DoesNotExist:
        return False


def checkUserExists(username):
    '''
    return True if user exists
    '''
    return UserInfo.count(username) == 1
