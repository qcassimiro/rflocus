CREATE TABLE IF NOT EXISTS `real`
(
    `reid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `apid` TEXT    NOT NULL,
    `rssi` INTEGER NOT NULL,
    `posx` INTEGER NOT NULL,
    `posy` INTEGER NOT NULL,
    `posz` INTEGER NOT NULL,
    `time` TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS `calc` (
    `caid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `apid` TEXT    NOT NULL,
    `rssi` INTEGER NOT NULL,
    `posx` INTEGER NOT NULL,
    `posy` INTEGER NOT NULL,
    `posz` INTEGER NOT NULL,
    `time` TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS `ctrl` (
    `ctid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `rfid` TEXT    NOT NULL,
    `apid` TEXT    NOT NULL,
    `rssi` INTEGER NOT NULL,
    `time` TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS `arxyz` (
    `arid` TEXT    NOT NULL PRIMARY KEY UNIQUE,
    `minx` INTEGER NOT NULL,
    `miny` INTEGER NOT NULL,
    `minz` INTEGER NOT NULL,
    `maxx` INTEGER NOT NULL,
    `maxy` INTEGER NOT NULL,
    `maxz` INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS `apxyz`
(
    `apid` TEXT    NOT NULL PRIMARY KEY UNIQUE,
    `posx` INTEGER NOT NULL,
    `posy` INTEGER NOT NULL,
    `posz` INTEGER NOT NULL
);
