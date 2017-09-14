NAPS_RANGE = range(3, 10)
NAREAS_RANGE = range(1, 10)
LOGCONF = "logging.json"
PORT_DEFAULT = 5500
PORT_METAVAR = "[5000-6000]"
PORT_RANGE = range(5000, 6000)
RFLOCUS_URI = "/rflocus"
DATABASE = "rflocus.db"
CREATE_REAL = '''
CREATE TABLE IF NOT EXISTS `real` (
    `reid`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `apid`  TEXT NOT NULL,
    `rssi`  INTEGER NOT NULL,
    `posx`  INTEGER NOT NULL,
    `posy`  INTEGER NOT NULL,
    `time`  TEXT NOT NULL UNIQUE,
    PRIMARY KEY(`reid`));
'''
CREATE_CALC = '''
CREATE TABLE IF NOT EXISTS `calc` (
    `caid`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `apid`  TEXT NOT NULL,
    `rssi`  INTEGER NOT NULL,
    `posx`  INTEGER NOT NULL,
    `posy`  INTEGER NOT NULL,
    `time`  TEXT NOT NULL UNIQUE,
    PRIMARY KEY(`caid`));
'''
CREATE_ARXY = '''
CREATE TABLE IF NOT EXISTS `arxy` (
    `arid`  TEXT NOT NULL UNIQUE,
    `minx`  INTEGER NOT NULL,
    `miny`  INTEGER NOT NULL,
    `maxx`  INTEGER NOT NULL,
    `maxy`  INTEGER NOT NULL,
    PRIMARY KEY(`arid`));
'''
CREATE_APXY = '''
CREATE TABLE IF NOT EXISTS `apxy` (
    `apid`  TEXT NOT NULL UNIQUE,
    `posx`  INTEGER NOT NULL,
    `posy`  INTEGER NOT NULL,
    PRIMARY KEY(`apid`));
'''
EXISTS_REAL = '''
SELECT name FROM sqlite_master WHERE type='table' AND name='real';
'''
EXISTS_CALC = '''
SELECT name FROM sqlite_master WHERE type='table' AND name='calc';
'''
EXISTS_ARXY = '''
SELECT name FROM sqlite_master WHERE type='table' AND name='arxy';
'''
EXISTS_APXY = '''
SELECT name FROM sqlite_master WHERE type='table' AND name='apxy';
'''
INSERT_REAL = '''
INSERT INTO `real` (`apid`, `rssi`, `posx`, `posy`, `time`)
VALUES (?, ?, ?, ?, ?);
'''
INSERT_CALC = '''
INSERT INTO `calc` (`apid`, `rssi`, `posx`, `posy`, `time`)
VALUES (?, ?, ?, ?, ?);
'''
INSERT_ARXY = '''
INSERT INTO `calc` (`arid`, `minx`, `miny`, `maxx`, `maxy`)
VALUES (?, ?, ?, ?, ?);
'''
INSERT_APXY = '''
INSERT INTO `calc` (`apid`, `posx`, `posy`)
VALUES (?, ?, ?);
'''
ISEMPTY_REAL = '''
SELECT COUNT(*) from `real`;
'''
ISEMPTY_CALC = '''
SELECT COUNT(*) from `calc`;
'''
ISEMPTY_ARXY = '''
SELECT COUNT(*) from `arxy`;
'''
ISEMPTY_APXY = '''
SELECT COUNT(*) from `apxy`;
'''
