create database ECE1779;

drop table if exists ECE1779.ImageInfo;
drop table if exists ECE1779.UserInfo;

create table ECE1779.UserInfo (
	id BIGINT AUTO_INCREMENT,
	username VARCHAR(128) NULL,
	`password` VARCHAR(256) NULL,
  email VARCHAR(256) NULL,
	PRIMARY KEY (id)) ENGINE=innodb;

create table ECE1779.ImageInfo(
	id BIGINT AUTO_INCREMENT,
  user_id BIGINT NULL,
  name VARCHAR(256) NULL,
  path VARCHAR(256) NULL,
  thumbnail_path VARCHAR(256) NULL,
  FOREIGN KEY (user_id) REFERENCES ECE1779.UserInfo(id),
  PRIMARY KEY (id)) ENGINE=innodb;
