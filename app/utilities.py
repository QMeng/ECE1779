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


def create_thumbnail(source_file, userID):
    '''create thumbnail for the image uploaded by user'''
    with Image(filename=os.path.join(IMAGE_FOLDER, userID, source_file)) as img:
        new_width = img.width / (img.height / 50)
        img.resize(round(new_width), 50)
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, userID, source_file))
    return os.path.join(THUMBNAIL_FOLDER, userID, "thumbnail_" + source_file)


def check_dup(imageName, userID):
    '''check to see if there are image belong to the user in database that has the same name'''
    imageList = ImageContents.query.filter_by(user_id=userID).all()
    for image in imageList:
        if (image.name == imageName):
            return True
    return False
