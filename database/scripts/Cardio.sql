--
-- File generated with SQLiteStudio v3.4.17 on Wed Aug 13 16:24:33 2025
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Cardio
CREATE TABLE IF NOT EXISTS Cardio (
	Stage int not null,
    Body int not null,
    Sex int not null,
    Sessions int,
    Time varchar(255),
    primary key (Stage, Body, Sex)
);
INSERT INTO Cardio (Stage, Body, Sex, Sessions, Time) VALUES (0, 2, 0, 3, '12, 15, 12 minutes');
INSERT INTO Cardio (Stage, Body, Sex, Sessions, Time) VALUES (1, 2, 0, 4, '22, 25, 22, 25 minutes');
INSERT INTO Cardio (Stage, Body, Sex, Sessions, Time) VALUES (0, 3, 0, 3, '15, 20, 15 minutes');
INSERT INTO Cardio (Stage, Body, Sex, Sessions, Time) VALUES (1, 3, 0, 4, '27, 30, 27, 30 minutes');
INSERT INTO Cardio (Stage, Body, Sex, Sessions, Time) VALUES (0, 4, 0, 3, '20, 20, 20 minutes');
INSERT INTO Cardio (Stage, Body, Sex, Sessions, Time) VALUES (1, 4, 0, 4, '35, 40, 30, 45 minutes');
INSERT INTO Cardio (Stage, Body, Sex, Sessions, Time) VALUES (0, 2, 1, 3, '12, 15, 12 minutes');
INSERT INTO Cardio (Stage, Body, Sex, Sessions, Time) VALUES (1, 2, 1, 4, '20, 22, 20, 22 minutes');
INSERT INTO Cardio (Stage, Body, Sex, Sessions, Time) VALUES (0, 3, 1, 3, '15, 20, 15 minutes');
INSERT INTO Cardio (Stage, Body, Sex, Sessions, Time) VALUES (1, 3, 1, 4, '25, 27, 25, 27 minutes');
INSERT INTO Cardio (Stage, Body, Sex, Sessions, Time) VALUES (0, 4, 1, 3, '20, 20, 20 minutes');
INSERT INTO Cardio (Stage, Body, Sex, Sessions, Time) VALUES (1, 4, 1, 4, '30, 35, 30, 35 minutes');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
