/*
	Moffat Bay Lodge
    Module 4 - Customer Table
    Description: Creates and populates Customer table 
*/

DROP TABLE IF EXISTS Customer;

CREATE TABLE Customer (
	UserID INT(10) NOT NULL AUTO_INCREMENT,
    Email varchar(255) UNIQUE,
    Password_Hash varchar(255),
    First_Name varchar(255),
    Last_Name varchar(255),
    Phone_Number varchar(20),
    PRIMARY KEY (UserID)
);

INSERT INTO Customer (Email, Password_Hash, First_Name, Last_Name, Phone_Number)
VALUES
	('jerrysmith97@hotmail.com', SHA2('password1', 256), 'Jerry', 'Smith', '8887776666'),
    ('yol_night@outlook.com', SHA2('password2', 256), 'Yolanda', 'Night', '8887776665'),
    ('tjones33@outlook.com', SHA2('password3', 256), 'Tim', 'Jones', '8887776664');