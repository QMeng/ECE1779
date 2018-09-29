from app import *
from wand.image import Image


def createImageFolder():
    '''create folder to store images uploaded by the user
        the location should be [project dir]/images
    '''
    if not os.path.isdir(IMAGE_FOLDER):
        os.mkdir(IMAGE_FOLDER)

def createThumbnailFolder():
    '''create folder to store thumbnails of the images uploaded by the user
        the location should be [project dir]/thumbnails
    '''
    if not os.path.isdir(THUMBNAIL_FOLDER):
        os.mkdir(THUMBNAIL_FOLDER)

def create_thumbnail(source_file):
    '''create thumbnail for the image uploaded by user'''
    with Image(filename=IMAGE_FOLDER + '/' + source_file) as img:
        new_width = img.width / (img.height / 50)
        img.resize(round(new_width), 50)
        img.save(filename=THUMBNAIL_FOLDER + "/thumbnail_" + source_file)
    return THUMBNAIL_FOLDER + "/thumbnail_" + source_file