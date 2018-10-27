import ctypes
from builtins import round

import botocore

from app_worker.models import *
from wand.image import Image
from wand.api import library
import glob


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
        uploadIntoS3(userID, os.path.join(THUMBNAIL_FOLDER, userID, thumbnailName), thumbnailName, False)

    with Image(filename=os.path.join(IMAGE_FOLDER, userID, rightshiftName)) as img:
        # resize the image to produce the thumbnail
        new_width = img.width / (img.height / 250)
        img.resize(round(new_width), 250)
        thumbnailName = "thumbnail_" + rightshiftName
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, userID, thumbnailName))
        uploadIntoS3(userID, os.path.join(THUMBNAIL_FOLDER, userID, thumbnailName), thumbnailName, False)

    with Image(filename=os.path.join(IMAGE_FOLDER, userID, blackAndWhiteName)) as img:
        # resize the image to produce the thumbnail
        new_width = img.width / (img.height / 250)
        img.resize(round(new_width), 250)
        thumbnailName = "thumbnail_" + blackAndWhiteName
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, userID, thumbnailName))
        uploadIntoS3(userID, os.path.join(THUMBNAIL_FOLDER, userID, thumbnailName), thumbnailName, False)

    with Image(filename=os.path.join(IMAGE_FOLDER, userID, sepiaName)) as img:
        # resize the image to produce the thumbnail
        new_width = img.width / (img.height / 250)
        img.resize(round(new_width), 250)
        thumbnailName = "thumbnail_" + sepiaName
        img.save(filename=os.path.join(THUMBNAIL_FOLDER, userID, thumbnailName))
        uploadIntoS3(userID, os.path.join(THUMBNAIL_FOLDER, userID, thumbnailName), thumbnailName, False)

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
        uploadIntoS3(userID, os.path.join(IMAGE_FOLDER, userID, rightshiftName), rightshiftName, True)

    with Image(filename=os.path.join(IMAGE_FOLDER, userID, pictureName)) as img:
        img.type = 'grayscale';
        img.save(filename=os.path.join(IMAGE_FOLDER, userID, blackAndWhiteName))
        uploadIntoS3(userID, os.path.join(IMAGE_FOLDER, userID, blackAndWhiteName), blackAndWhiteName, True)

    with Image(filename=os.path.join(IMAGE_FOLDER, userID, pictureName)) as img:
        library.MagickSepiaToneImage.argtypes = [ctypes.c_void_p, ctypes.c_double]
        library.MagickSepiaToneImage.restype = None
        threshold = img.quantum_range * 0.8
        library.MagickSepiaToneImage(img.wand, threshold)
        img.save(filename=os.path.join(IMAGE_FOLDER, userID, sepiaName))
        uploadIntoS3(userID, os.path.join(IMAGE_FOLDER, userID, sepiaName), sepiaName, True)

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


def uploadIntoS3(userID, filePath, fileName, isImage):
    '''
    Upload image into S3 bucket
    :param userID: user id of current user
    :param filePath: path leading to the file that we want to upload
    :param fileName: file name
    :param isImage: set to true if it is image, set to false if it is thumbnail
    '''
    if isImage:
        bucketName = IMAGE_BUCKET_PREFIX + userID
    else:
        bucketName = THUMBNAIL_BUCKET_PREFIX + userID

    if (not checkBucketExist(bucketName)):
        s3.create_bucket(Bucket=bucketName)
    s3.Bucket(bucketName).upload_file(Filename=filePath, Key=fileName)


def downloadFromS3(userID, bucketName, isImage):
    '''
    download specific bucket from S3
    :param userID: current user id
    :param bucketName: bucket's name
    :param isImage: set to true if want to download image bucket, set to false if want to download thumbnail bucket
    :return:
    '''
    if checkBucketExist(bucketName):
        bucket = s3.Bucket(bucketName)
        if isImage:
            createImageFolder(userID)
            folderBase = IMAGE_FOLDER
        else:
            createThumbnailFolder(userID)
            folderBase = THUMBNAIL_FOLDER

        for obj in bucket.objects.all():
            path, filename = os.path.split(obj.key)
            bucket.download_file(obj.key, os.path.join(folderBase, userID, filename))


def checkBucketExist(bucketName):
    '''
    check if specific s3 bucket exists or not
    '''
    try:
        s3.meta.client.head_bucket(Bucket=bucketName)
        return True
    except botocore.exceptions.ClientError as e:
        return False


def wipeOutLocalImage(userID):
    '''
    remove all the user's files from local
    '''
    if os.path.isdir(os.path.join(IMAGE_FOLDER, userID)):
        files = glob.glob(os.path.join(IMAGE_FOLDER, userID, '*'))
        for file in files:
            os.remove(file)
    if os.path.isdir(os.path.join(THUMBNAIL_FOLDER, userID)):
        files = glob.glob(os.path.join(THUMBNAIL_FOLDER, userID, '*'))
        for file in files:
            os.remove(file)
    os.removedirs(os.path.join(IMAGE_FOLDER, userID))
    os.removedirs(os.path.join(THUMBNAIL_FOLDER, userID))
