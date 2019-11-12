CREATE DATABASE IF NOT EXISTS flaskapp;
USE flaskapp;
CREATE TABLE IF NOT EXISTS `users` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `email` varchar(320) NOT NULL,
	  `username` varchar(32) NOT NULL,
	  `password` varchar(32) NOT NULL,
	  `is_admin` tinyint(1) DEFAULT '0',
	  PRIMARY KEY (`id`)
);
CREATE TABLE IF NOT EXISTS `requests` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `user_id` int(11) NOT NULL,
	  `type` varchar(30) NOT NULL,
	  `approved` tinyint(1) DEFAULT '0',
	  PRIMARY KEY (`id`)
);
CREATE USER IF NOT EXISTS 'flask'@'localhost';
GRANT ALL ON `flaskapp`.* TO 'flask'@'localhost'
