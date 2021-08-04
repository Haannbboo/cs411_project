flightsTable = """
CREATE TABLE flights (
    id int NOT NULL,
    FlightNumber VARCHAR(50),
    Airplane VARCHAR(100),
    Airline VARCHAR(255),
    deptTime DATETIME,
    deptAirport VARCHAR(20),
    arrTime DATETIME,
    arrAirport VARCHAR(20),
    Price int,
    AvailableSeats int DEFAULT 0,
    PRIMARY KEY(id)
);
"""
usersTable = """
CREATE TABLE users (
    uid int,
    username VARCHAR(255),
    pwd VARCHAR(255),
    email VARCHAR(255),
    role VARCHAR(50),
    PRIMARY KEY(uid)
);
"""

bookingsTable = """
CREATE TABLE bookings (
    bid int,
    uid int,
    fid int,
    price int,
    bookTime datetime,
    bookLevel int,
    PRIMARY KEY(bid),
    FOREIGN KEY(uid) REFERENCES users(uid) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(fid) REFERENCES flights(id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""

setIsolationLevel = "SET GLOBAL TRANSACTION ISOLATION LEVEL REPEATABLE READ;"


insertTrig = """
CREATE TRIGGER insertTrig
    BEFORE INSERT ON flights
    FOR EACH ROW
    BEGIN
        IF EXISTS(SELECT id FROM flights WHERE FlightNumber = new.FlightNumber AND deptTime = new.deptTime) THEN
            SIGNAL SQLSTATE '45000';
        END IF;
        IF @flight IS NULL THEN
            SET @maxID = (SELECT MAX(id) FROM flights);
            SET new.id = @maxID + 1;
        END IF;
    END;
"""