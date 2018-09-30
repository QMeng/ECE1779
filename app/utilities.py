from app import *
from wand.image import Image




def createImageFolder():
    '''create folder to store images uploaded by the user
        the location should be [project dir]/images
    '''
    user_id = request.cookies.get('userId')
    if not os.path.isdir(IMAGE_FOLDER + user_id):
        os.mkdir(IMAGE_FOLDER + user_id)


def createThumbnailFolder():
    '''create folder to store thumbnails of the images uploaded by the user
        the location should be [project dir]/thumbnails
    '''
    user_id = request.cookies.get('userId')
    if not os.path.isdir(THUMBNAIL_FOLDER + user_id):
        os.mkdir(THUMBNAIL_FOLDER + user_id)


def create_thumbnail(source_file):
    '''create thumbnail for the image uploaded by user'''
    user_id = request.cookies.get('userId')
    uploaded_image = "/".join([IMAGE_FOLDER + user_id, source_file])
    with Image(filename=uploaded_image) as img:
        new_width = img.width / (img.height / 100)
        img.resize(round(new_width), 100)
        img.save(filename=THUMBNAIL_FOLDER + user_id+ "/thumbnail" + source_file)
    return THUMBNAIL_FOLDER + user_id + "/thumbnail" + source_file