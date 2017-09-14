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
    `time`  TEXT UNIQUE,
    PRIMARY KEY(`reid`)
);
'''
CREATE_CALC = '''
CREATE TABLE IF NOT EXISTS `calc` (
    `caid`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `apid`  TEXT NOT NULL,
    `rssi`  INTEGER NOT NULL,
    `posx`  INTEGER NOT NULL,
    `posy`  INTEGER NOT NULL,
    `time`  TEXT UNIQUE,
    PRIMARY KEY(`caid`)
);
'''
CREATE_ARXY = '''
CREATE TABLE IF NOT EXISTS `arxy` (
    `arid`  TEXT NOT NULL UNIQUE,
    `minx`  INTEGER NOT NULL,
    `miny`  INTEGER NOT NULL,
    `maxx`  INTEGER NOT NULL,
    `maxy`  INTEGER NOT NULL,
    PRIMARY KEY(`arid`)
);
'''
CREATE_APXY = '''
CREATE TABLE IF NOT EXISTS `apxy` (
    `apid`  TEXT NOT NULL UNIQUE,
    `posx`  INTEGER NOT NULL,
    `posy`  INTEGER NOT NULL,
    PRIMARY KEY(`apid`)
);
'''
