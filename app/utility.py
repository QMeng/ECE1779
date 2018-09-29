import os
from flask import *
from wand.image import Image

APP_ROOT = os.path.dirname(os.path.abspath(__file__))



def build_thum_dir():
    user = request.cookies.get('userId')
    target = os.path.join(APP_ROOT, 'thumbnails_' + user)
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    return target


def find_path():
    user = request.cookies.get('userId')
    target = os.path.join(APP_ROOT, 'thumbnails_' + user)
    for upload in request.files.getlist("file"):

        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, 'thumbnail_' + filename])
        print ("Accept incoming thumbnail file:", filename)
        print ("Save it to:",  destination)
    return destination


def create_thumbnail(source_file, width, height):
    with Image(filename=source_file) as img:
        img.resize(width, height)
        thum_path = build_thum_dir()
        os.chdir(thum_path)
        img.save(filename="thumbnail_" + source_file)


def check_duplication(upload_file):
    thum_path = build_thum_dir()
    os.chdir(thum_path)
    thum_images = os.listdir(APP_ROOT + '/images_' + request.cookies.get('userId'))
    for name in thum_images:
        print("the file contents are:{}".format(name))
        if name == upload_file:
           return render_template("error_page.html")



##def create_thumbnail(source_file, width, height):
##    with Image(width=width, height=height) as outerImg:
##        with Image(filename=source_file) as img:
##            img.transform(resize="%dx%d>" % (width, height))
##            outerImg.format = img.format.lower()
            ## outerImg.composite(img, left=(width - img.width) // 2, top=(height - img.height) // 2)
##            outerImg.composite(img, left=248, top=240)
 ##           thum_path = build_thum_dir()
 ##           os.chdir(thum_path)
 ##           outerImg.save(filename="thumbnail_" + source_file)


