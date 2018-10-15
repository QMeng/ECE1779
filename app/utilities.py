import ctypes
from builtins import round

from app.models import *
from wand.image import Image
from wand.api import library


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

    pictureName = computeFileName(source_file, '-1.')
    rightshiftName = computeFileName(source_file, '-2.')
    blackAndWhiteName = computeFileName(source_file, '-3.')
    sepiaName = computeFileName(source_file, '-4.')

    with Image(filename=os.path.join(IMAGE_FOLDER, userID, pictureName)) as img:
        # resize the image to produce the thumbnail
        new_width = img.width / (img.height / 250)
        img.resize(round(new_width), 250)
        thumbnailName = "thumbnail_" + pictureName
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, userID, thumbnailName))

    with Image(filename=os.path.join(IMAGE_FOLDER, userID, rightshiftName)) as img:
        # resize the image to produce the thumbnail
        new_width = img.width / (img.height / 250)
        img.resize(round(new_width), 250)
        thumbnailName = "thumbnail_" + rightshiftName
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, userID, thumbnailName))

    with Image(filename=os.path.join(IMAGE_FOLDER, userID, blackAndWhiteName)) as img:
        # resize the image to produce the thumbnail
        new_width = img.width / (img.height / 250)
        img.resize(round(new_width), 250)
        thumbnailName = "thumbnail_" + blackAndWhiteName
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, userID, thumbnailName))

    with Image(filename=os.path.join(IMAGE_FOLDER, userID, sepiaName)) as img:
        # resize the image to produce the thumbnail
        new_width = img.width / (img.height / 250)
        img.resize(round(new_width), 250)
        thumbnailName = "thumbnail_" + sepiaName
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, userID, thumbnailName))

    return os.path.join(THUMBNAIL_FOLDER, userID)


def create_transformations(source_file, userID):
    '''
    This methods creates ans saves 3 transformations of the source file: multishift of red and blue, black and white, sepia
    :param source_file:
    :param userID:
    :return: image folder path
    '''
    pictureName = computeFileName(source_file, '-1.')
    rightshiftName = computeFileName(source_file, '-2.')
    blackAndWhiteName = computeFileName(source_file, '-3.')
    sepiaName = computeFileName(source_file, '-4.')

    with Image(filename=os.path.join(IMAGE_FOLDER, userID, pictureName)) as img:
        img.evaluate(operator='rightshift', value=1, channel='blue')
        img.evaluate(operator='leftshift', value=1, channel='red')
        img.save(filename=os.path.join(IMAGE_FOLDER, userID, rightshiftName))

    with Image(filename=os.path.join(IMAGE_FOLDER, userID, pictureName)) as img:
        img.type = 'grayscale';
        img.save(filename=os.path.join(IMAGE_FOLDER, userID, blackAndWhiteName))

    with Image(filename=os.path.join(IMAGE_FOLDER, userID, pictureName)) as img:
        library.MagickSepiaToneImage.argtypes = [ctypes.c_void_p, ctypes.c_double]
        library.MagickSepiaToneImage.restype = None
        threshold = img.quantum_range * 0.8
        library.MagickSepiaToneImage(img.wand, threshold)
        img.save(filename=os.path.join(IMAGE_FOLDER, userID, sepiaName))

    return os.path.join(IMAGE_FOLDER, userID)


def check_dup(imageName, userID):
    '''check to see if there are image belong to the user in database that has the same name'''
    imageList = ImageContents.query.filter_by(user_id=userID).all()
    for image in imageList:
        if (image.name == imageName):
            return True
    return False

def computeFileName(imageName, trail):
    '''
    this method computes the correct actual file name of the image we are looking for.
    trail as 4 values: '-1.', '-2.', '-3.', '-4.', each representing the original, multishift, black and white, sepia
    '''
    nameAndType = imageName.split('.')
    fileName = "".join(nameAndType[:-1])
    fileType = nameAndType[-1]
    pictureName = fileName + trail + fileType
    return pictureName
