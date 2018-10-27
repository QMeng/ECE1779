This project is for ECE1779 - Cloud Computing - offered at University of Toronto 2018 fall semester.

The following sections will be an introduction of the project with some detailed layout.

Contributors/Group members (Name, UTorID, Student #):
Qingsong Meng,  mengqin6,   998383093
Shihan Liu,     liushih3,   1005056145
Zou Ming,       zouming2,   1003495611

Project introduction:
    This project builds a image uploading web application using flask, mysql, imagemagick, werkzeug.
    This web application lets registered users upload images into their accounts/pages, and creates 3 transformations 
    (MultiShift, Black & White, Sepia) for the uploaded images. For new users, there is option for sign up as well.
    The web application is deployed on an AWS instance created with provided AMI. Deployment instructions and AWS
    credentials are stored in deployment.txt.

How to access the web application (after deployment):
    Port 8080 of the AWS instance is opened for HTTP access.
    1. From the AWS instance, open any type of browser (firefox), type 'http://0.0.0.0:8080/' in the address bar.
    2. From your computer, open any type of browser, type 'http//<public ip of aws instance>:8080/' in the address bar.

Project structure layout:
    ECE1779A1
        -> imageUploader.py
        -> venv/
        -> images/ (will be created after web app started running)
        -> thumbnails/ (will be created after web app started running)
        -> run.sh
        -> ECE1779.sql
        -> app
            -> static
                -> *.css
                -> *.js
            -> templates
                -> *.html
            -> __init__.py
            -> config.py
            -> forms.py
            -> models.py
            -> routes.py
            -> utilities.py

Detailed project structure:
    1.  imageUploader.py contains the main function of this web app.
    2.  venv folder contains all the python libraries used in this project. Including: flask, flask-login, flask-wtf,
        flask-sqlalchemy, werkzeug, pymysql, wand (api binding for ImageMagick), etc.
    3.  images and thumbnails folders will be used to store the images (and transformations) uploaded by the users and
        thumbnails (of original image and transformed images).
    4.  run.sh is the script for spinning up the virtual environment and kick off the web app.
    5.  ECE1779.sql contains sql scripts for creating the database, tables used by this project. Table schema will be
        listed in later sections.
    6.  app folder contains the scripts that make this web app work.
    7.  app/static folder contains css and javascript files that used by the front end UI of the web app.
    8.  app/templates folder contains the HTML files used for the web app's front end UI display. Combined with files
        under app/static folder, the front end UI display of this project is completed.
    9.  app/__init__.py initializes the flask app object that is used across almost all the scripts. It also contains
        multiple global variables that will be referred in other scripts.
    10. app/config.py stores all the configurations for the flask app, including database credentials, etc.
    11. app/forms.py stores object classes for the login, signup, file upload forms. These objects is integrated with
        the front end forms that were displayed on the web pages, so the values will be extracted and feed into these
        objects. Form fields has validations on them, for example, in sign up form, password field and repeat password
        field must have the same value.
    12. app/models.py stores User and ImageContent object classes, information stored in these 2 objects will be feed
        into mysql database. Note: the password field in User object will be first appended with a random salt value,
        then hashed, before committed into database.
    13. app/routes.py contains all the definitions for the routes in this web app. All the request handling are
        happening in this file, like sign up requests, user login requests, receiving form info, receiving uploaded
        file and store them, etc. There are 2 types of routes, one is pages that is visible, or in other words,
        rendered with html templates under app/templates, the other kind is hidden api endpoint, like the project
        requirement, '/test/FileUpload' URI is not accessible through front end, but it can receive post requests sent
        by API client (for example, Postman).
    14. app/utilities.py contains utility functions like creating thumbnails, creating transformations for images, etc.

/test/FileUpload URI:
    This is the URI for automatic image uploading. This URI was implemented exactly according to the requirements listed
    on the project page.

    relative URL = /test/FileUpload
    enctype = multipart/form-data
    method = post
    field1 name = userID type = string
    field2 name = password type = string
    field2 name = uploadedfile type = file

Database table schema:
    2 tables were created and used in this project. UserInfo is used for storing user information. ImageInfo is used
    for storing image information.

    UserInfo
        id - primary key of this table
	    username - user name
	    password - hash value of the password + salt
	    email - email address of the user

    ImageInfo
        id - primary key of this table
        user_id - foreign key referencing UserInfo table
        name - image's name
        path - absolute path of where this image (and its transformations) is stored
        thumbnail_path - absolute path of where the thumbnails of this image is stored
