from builtins import round
from app.models import *
from wand.image import Image


def createImageFolder(userID):
    '''create folder to store images uploaded by the user
        the location should be [project dir]/images
    '''
    if not os.path.isdir(IMAGE_FOLDER):
        os.mkdir(IMAGE_FOLDER)
    if not os.path.isdir(os.path.join(IMAGE_FOLDER, userID)):
        os.mkdir(os.path.join(IMAGE_FOLDER, userID))


def createThumbnailFolder(userID):
    '''create folder to store thumbnails of the images uploaded by the user
        the location should be [project dir]/thumbnails
    '''
    if not os.path.isdir(THUMBNAIL_FOLDER):
        os.mkdir(THUMBNAIL_FOLDER)
    if not os.path.isdir(os.path.join(THUMBNAIL_FOLDER, userID)):
        os.mkdir(os.path.join(THUMBNAIL_FOLDER, userID))

def createTransformationFolder():
    '''create folder to store transformation of the images uploaded by the user
        the location should be [project dir]/thumbnails
    '''
    user_id = request.cookies.get('userId')
    if not os.path.isdir(TRANSFORM_FOLDER + user_id):
        os.mkdir(TRANSFORM_FOLDER + user_id)

def createTransThumbnailFolder():
    '''create folder to store transformation of the thumbnails uploaded by the user
        the location should be [project dir]/thumbnails
    '''
    user_id = request.cookies.get('userId')
    if not os.path.isdir(TRANS_THUMB_FOLDER + user_id):
        os.mkdir(TRANS_THUMB_FOLDER + user_id)

def createPictureTransThumbFolder(filename):
    '''create folder to store transformation of the thumbnails uploaded by the user
        the location should be [project dir]/thumbnails
    '''
    user_id = request.cookies.get('userId')
    without_ext = os.path.splitext(filename)[0]
    if not os.path.isdir(TRANS_THUMB_FOLDER + user_id + '/' + without_ext):
        os.mkdir(TRANS_THUMB_FOLDER + user_id + '/' + without_ext)


def create_thumbnail(source_file, userID):
    '''create thumbnail for the image uploaded by user'''


    with Image(filename=os.path.join(IMAGE_FOLDER, userID, source_file)) as img:
        new_width = img.width / (img.height / 50)
        img.resize(round(new_width), 50)
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, userID, "thumbnail_" + source_file))
    return os.path.join(THUMBNAIL_FOLDER, userID, "thumbnail_" + source_file)


def create_trans_thumbnail(source_file, origin_file):
    '''create thumbnail for the tranformed image'''
    user_id = request.cookies.get('userId')
    uploaded_image = "/".join([TRANSFORM_FOLDER + user_id, source_file])
    without_ext = os.path.splitext(origin_file)[0]
    with Image(filename=uploaded_image) as img:
        new_width = img.width / (img.height / 100)
        img.resize(round(new_width), 100)
        img.save(filename=TRANS_THUMB_FOLDER + user_id + "/" + without_ext + "/thumbnail" + source_file)
    return THUMBNAIL_FOLDER + user_id + "/" + without_ext + "/thumbnail" + source_file


def create_transform1(source_file):# level
    '''create the first transformation both full-size image and its thumbnails.
    Suppose the original file name is: example.jpg or example_thumbnails.jpg,
    the name of the image will be: trans2_example.jpg or trans2_example_thumbnails.jpg
    '''
    user_id = request.cookies.get('userId')
    #without_ext = os.path.splitext(source_file)[0]
    uploaded_image = "/".join([IMAGE_FOLDER + user_id, source_file])
    with Image(filename=uploaded_image) as img:
        img.level(black=0.5, white=0.5, gamma=0.5)
        img.save(filename=TRANSFORM_FOLDER + user_id + '/' + "/trans1" + source_file)
    return TRANSFORM_FOLDER + user_id + '/' + "/trans1" + source_file


def create_transform2(source_file):#rotate
    '''create the second transformation both full-size image and its thumbnails.
    Suppose the original file name is: example.jpg or example_thumbnails.jpg,
    the name of the image will be: trans2_example.jpg or trans2_example_thumbnails.jpg
    '''
    user_id = request.cookies.get('userId')
    #without_ext = os.path.splitext[0]
    uploaded_image = "/".join([IMAGE_FOLDER + user_id, source_file])
    with Image(filename=uploaded_image) as img:
        img.rotate(90)
        img.save(filename=TRANSFORM_FOLDER + user_id + '/' + "/trans2" + source_file)
    return TRANSFORM_FOLDER + user_id + '/' + "/trans2" + source_file


def check_dup(imageName, userID):
    '''check to see if there are image belong to the user in database that has the same name'''
    imageList = ImageContents.query.filter_by(user_id=userID).all()
    for image in imageList:
        if (image.name == imageName):
            return True
    return False
