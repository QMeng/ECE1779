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
        # resize the image to produce the thumbnail
        new_width = img.width / (img.height / 100)
        img.resize(round(new_width), 100)
        thumbnailName = "thumbnail_" + source_file
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, userID, thumbnailName))
    return os.path.join(THUMBNAIL_FOLDER, userID)


def create_rightshift(source_file, userID):
    '''create a level transformation for the image uploaded by user'''
    nameAndType = source_file.split('.')
    fileName = "".join(nameAndType[:-1])
    fileType = nameAndType[-1]
    pictureName = fileName + '-1.' + fileType
    with Image(filename=os.path.join(IMAGE_FOLDER, userID, pictureName)) as img:
        # create a rightshift image
        img.evaluate(operator='rightshift', value=1, channel='blue')
        save_name = fileName + "-2." + fileType
        img.save(filename=os.path.join(IMAGE_FOLDER, userID, save_name))
    return os.path.join(IMAGE_FOLDER, userID)


def create_leftshift(source_file, userID):
    '''create a left shift transformation for the image uploaded by user'''
    nameAndType = source_file.split('.')
    fileName = "".join(nameAndType[:-1])
    fileType = nameAndType[-1]
    pictureName = fileName + '-1.' + fileType
    with Image(filename=os.path.join(IMAGE_FOLDER, userID, pictureName)) as img:
        # create a leftshift image
        img.evaluate(operator='leftshift', value=1, channel='red')
        save_name = fileName + "-3." + fileType
        img.save(filename=os.path.join(IMAGE_FOLDER, userID, save_name))
    return os.path.join(IMAGE_FOLDER, userID)


def check_dup(imageName, userID):
    '''check to see if there are image belong to the user in database that has the same name'''
    imageList = ImageContents.query.filter_by(user_id=userID).all()
    for image in imageList:
        if (image.name == imageName):
            return True
    return False
