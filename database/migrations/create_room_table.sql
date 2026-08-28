/*
    Moffat Bay Lodge
    Module 4 - Room Table
    Description: Creates the Room table based on the team ERD.
*/

CREATE TABLE Room (
    RoomID INT(10) NOT NULL AUTO_INCREMENT,
    Description VARCHAR(255),
    Name VARCHAR(255),
    Price DECIMAL(6,2),
    Status VARCHAR(255),
    PRIMARY KEY (RoomID)
);