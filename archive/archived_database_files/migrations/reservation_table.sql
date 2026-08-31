/*
    Moffat Bay Lodge
    Module 4 - Reservation Table and Data
    Description: Create Reservation table from ERD and add 3 reservations
	Execution Order: Noors Room Table/Data, Carlis Customer Table and Data, Justins Reservation Table/Data
	Note: Noor's and Carli's files can be ran first or second. This file has to be ran last due to foreign keys.
*/

-- Drop table if it exists to prevent duplications
DROP TABLE IF EXISTS Reservation;

-- Create the Reservation Table
CREATE TABLE Reservation (
    ReservationID INT(10) NOT NULL AUTO_INCREMENT,
    UserID INT(10) NOT NULL,
    RoomID INT(10) NOT NULL,
    Booking_Date DATE NOT NULL,
    Date_In DATE NOT NULL,
    Date_Out DATE NOT NULL,
    Guest_Count INT(10) NOT NULL,
    PRIMARY KEY (ReservationID),
    CONSTRAINT fk_customer
        FOREIGN KEY (UserID)
        REFERENCES Customer(UserID),
    CONSTRAINT fk_room
        FOREIGN KEY (RoomID)
        REFERENCES Room(RoomID)
);

-- Insert Reservation Record
INSERT INTO Reservation
    (UserID, RoomID, Booking_Date, Date_In, Date_Out, Guest_Count)
VALUES
    (1, 2, '2026-08-27', '2026-08-28', '2026-08-31', 4);
