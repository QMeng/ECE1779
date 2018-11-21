import ctypes
from builtins import round

import botocore
from pynamodb.exceptions import DoesNotExist

from app_musicUploader.models import *
from wand.image import Image
from wand.api import library
import glob


def createImageFolder(username):
    '''create folder to store images uploaded by the user
        the location should be [project dir]/images
    '''
    if not os.path.isdir(IMAGE_FOLDER):
        os.mkdir(IMAGE_FOLDER)
    if not os.path.isdir(os.path.join(IMAGE_FOLDER, username)):
        os.mkdir(os.path.join(IMAGE_FOLDER, username))


def createThumbnailFolder(username):
    '''create folder to store thumbnails of the images uploaded by the user
        the location should be [project dir]/thumbnails
    '''
    if not os.path.isdir(THUMBNAIL_FOLDER):
        os.mkdir(THUMBNAIL_FOLDER)
    if not os.path.isdir(os.path.join(THUMBNAIL_FOLDER, username)):
        os.mkdir(os.path.join(THUMBNAIL_FOLDER, username))


def create_thumbnail(source_file, username):
    '''create thumbnail for the image uploaded by user'''

    pictureName = computeFileName(source_file, '-1.')
    rightshiftName = computeFileName(source_file, '-2.')
    blackAndWhiteName = computeFileName(source_file, '-3.')
    sepiaName = computeFileName(source_file, '-4.')

    # creating, saving and uploadind into S3 for the thumbnails for original and 3 transformations
    with Image(filename=os.path.join(IMAGE_FOLDER, username, pictureName)) as img:
        # resize the image to produce the thumbnail
        new_width = img.width / (img.height / 250)
        img.resize(round(new_width), 250)
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, username, pictureName))
        uploadIntoS3(username, os.path.join(THUMBNAIL_FOLDER, username, pictureName), pictureName, False)

    with Image(filename=os.path.join(IMAGE_FOLDER, username, rightshiftName)) as img:
        # resize the image to produce the thumbnail
        new_width = img.width / (img.height / 250)
        img.resize(round(new_width), 250)
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, username, rightshiftName))
        uploadIntoS3(username, os.path.join(THUMBNAIL_FOLDER, username, rightshiftName), rightshiftName, False)

    with Image(filename=os.path.join(IMAGE_FOLDER, username, blackAndWhiteName)) as img:
        # resize the image to produce the thumbnail
        new_width = img.width / (img.height / 250)
        img.resize(round(new_width), 250)
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, username, blackAndWhiteName))
        uploadIntoS3(username, os.path.join(THUMBNAIL_FOLDER, username, blackAndWhiteName), blackAndWhiteName, False)

    with Image(filename=os.path.join(IMAGE_FOLDER, username, sepiaName)) as img:
        # resize the image to produce the thumbnail
        new_width = img.width / (img.height / 250)
        img.resize(round(new_width), 250)
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, username, sepiaName))
        uploadIntoS3(username, os.path.join(THUMBNAIL_FOLDER, username, sepiaName), sepiaName, False)

    return THUMBNAIL_BUCKET_PREFIX + username


def create_transformations(source_file, username):
    '''
    This methods creates ans saves 3 transformations of the source file: multishift of red and blue, black and white, sepia
    :param source_file:
    :param username:
    :return: image folder path
    '''
    pictureName = computeFileName(source_file, '-1.')
    rightshiftName = computeFileName(source_file, '-2.')
    blackAndWhiteName = computeFileName(source_file, '-3.')
    sepiaName = computeFileName(source_file, '-4.')

    # creating, saving and uploading into S3 for the 3 transformations
    with Image(filename=os.path.join(IMAGE_FOLDER, username, pictureName)) as img:
        img.evaluate(operator='rightshift', value=1, channel='blue')
        img.evaluate(operator='leftshift', value=1, channel='red')
        img.save(filename=os.path.join(IMAGE_FOLDER, username, rightshiftName))
        uploadIntoS3(username, os.path.join(IMAGE_FOLDER, username, rightshiftName), rightshiftName, True)

    with Image(filename=os.path.join(IMAGE_FOLDER, username, pictureName)) as img:
        img.type = 'grayscale';
        img.save(filename=os.path.join(IMAGE_FOLDER, username, blackAndWhiteName))
        uploadIntoS3(username, os.path.join(IMAGE_FOLDER, username, blackAndWhiteName), blackAndWhiteName, True)

    with Image(filename=os.path.join(IMAGE_FOLDER, username, pictureName)) as img:
        library.MagickSepiaToneImage.argtypes = [ctypes.c_void_p, ctypes.c_double]
        library.MagickSepiaToneImage.restype = None
        threshold = img.quantum_range * 0.8
        library.MagickSepiaToneImage(img.wand, threshold)
        img.save(filename=os.path.join(IMAGE_FOLDER, username, sepiaName))
        uploadIntoS3(username, os.path.join(IMAGE_FOLDER, username, sepiaName), sepiaName, True)

    return IMAGE_BUCKET_PREFIX + username


def check_dup(imageName, username):
    '''check to see if there are image belong to the user in database that has the same name'''
    imageList = ImageInfo.query(username)
    for image in imageList:
        if image.imagename == imageName:
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


def uploadIntoS3(username, filePath, fileName, isImage):
    '''
    Upload image into S3 bucket
    :param username: user id of current user
    :param filePath: path leading to the file that we want to upload
    :param fileName: file name
    :param isImage: set to true if it is image, set to false if it is thumbnail
    '''
    if isImage:
        bucketName = IMAGE_BUCKET_PREFIX + username
    else:
        bucketName = THUMBNAIL_BUCKET_PREFIX + username

    if (not checkBucketExist(bucketName)):
        s3_resource.create_bucket(Bucket=bucketName)
    s3_resource.Bucket(bucketName).upload_file(Filename=filePath, Key=fileName)


def downloadFromS3(username, bucketName, isImage):
    '''
    download specific bucket from S3
    :param username: current user id
    :param bucketName: bucket's name
    :param isImage: set to true if want to download image bucket, set to false if want to download thumbnail bucket
    :return:
    '''
    if checkBucketExist(bucketName):
        bucket = s3_resource.Bucket(bucketName)
        if isImage:
            createImageFolder(username)
            folderBase = IMAGE_FOLDER
        else:
            createThumbnailFolder(username)
            folderBase = THUMBNAIL_FOLDER

        for obj in bucket.objects.all():
            path, filename = os.path.split(obj.key)
            bucket.download_file(obj.key, os.path.join(folderBase, username, filename))


def checkBucketExist(bucketName):
    '''
    check if specific s3 bucket exists or not
    '''
    try:
        s3_resource.meta.client.head_bucket(Bucket=bucketName)
        return True
    except botocore.exceptions.ClientError as e:
        return False


def wipeOutLocalImage(username):
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


def getUserOriginalImages(username):
    '''
    get the original images belong to this user in the database
    '''
    images = ImageInfo.query(username)
    keys = []
    for image in images:
        keys.append(computeFileName(image.imagename, '-1.'))

    return keys


def getUserImages(username):
    '''
    get all the images belong to this user in the database
    '''
    images = ImageInfo.query(username)
    keys = []
    for image in images:
        keys.append(computeFileName(image.imagename, '-1.'))
        keys.append(computeFileName(image.imagename, '-2.'))
        keys.append(computeFileName(image.imagename, '-3.'))
        keys.append(computeFileName(image.imagename, '-4.'))

    return keys


def getPresignedUrl(username, image_list, isImage):
    '''
    compute the presigned urls for the images in S3
    '''
    if isImage:
        bucket = IMAGE_BUCKET_PREFIX + username
    else:
        bucket = THUMBNAIL_BUCKET_PREFIX + username

    urls = []
    for image in image_list:
        url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': image})
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
    return UserInfo.query(username) == 1
