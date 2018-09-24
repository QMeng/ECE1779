create database ECE1779A1;

create table ECE1779A1.UserInfo (
	user_id BIGINT AUTO_INCREMENT,
	user_username VARCHAR(128) NULL,
	user_password VARCHAR(256) NULL,
    user_email VARCHAR(256) NULL,
	PRIMARY KEY (user_id));

create table ECE1779A1.ImageInfo(
	image_id BIGINT AUTO_INCREMENT,
    user_id BIGINT NULL,
    image_name VARCHAR(256) NULL,
    image_path VARCHAR(256) NULL,
    image_thumbnail_path VARCHAR(256) NULL,
    FOREIGN KEY (user_id) REFERENCES ECE1779A1.UserInfo(user_id),
    PRIMARY KEY (image_id));