#!/usr/bin/python3


import errno
import os
import sqlite3

PATH = "rflocus.db"
SCHEMA = "database/schema.sql"
STDATA = "database/stdata.sql"

ACCESS_POINTS_RANGE = range(4, 8)
AREAS_RANGE = range(2, 8)


class RFLDatabase():
    def __init__(self):
        self.connection = sqlite3.connect(PATH)
        self.cursor = self.connection.cursor()
        if not self.built():
            self.load_script(SCHEMA)
        if not self.ready():
            self.load_script(STDATA)

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def has_table(self, table):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(
            table)
        self.cursor.execute(query)
        return True if self.cursor.fetchall() else False

    def built(self):
        return (self.has_table('arxyz') and
                self.has_table('apxyz') and
                self.has_table('real') and
                self.has_table('calc') and
                self.has_table('ctrl'))

    def count(self, table):
        query = "SELECT COUNT(*) FROM `" + table + "`;"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def ready(self):
        return self.count('arxyz') in AREAS_RANGE and self.count('apxyz') in ACCESS_POINTS_RANGE

    def load_script(self, script):
        if os.path.exists(script):
            with open(script, 'rt') as f:
                query = f.read()
                self.cursor.executescript(query)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), script)

    def get_references(self, apids):
        query = "SELECT * FROM `apxyz` WHERE `apid` IN " + tuple(str(apids)) + ";"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_area(self, posxyz):
        query = '''SELECT `arid` FROM `arxyz` WHERE
        `minx` < {} and `maxx` > {} and
        `miny` < {} and `maxy` > {} and
        `minz` < {} and `maxz` > {}'''.format(posxyz[0], posxyz[0], posxyz[1], posxyz[1], posxyz[2], posxyz[2])
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0] if result else None

    def put_real(self, record):
        query = '''INSERT INTO `real` (`apid`, `rssi`, `posx`, `posy`, `posz`, `time`) VALUES
        ('{}', {}, {}, {}, {}, '{}')'''.format(record['apid'], record['rssi'], record['posx'],
                                               record['posy'], record['posz'], record['time'])
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if result else None

    def put_calc(self, record):
        query = '''INSERT INTO `calc` (`apid`, `rssi`, `posx`, `posy`, `posz`, `time`) VALUES
        ('{}', {}, {}, {}, {}, '{}')'''.format(record['apid'], record['rssi'], record['posx'],
                                               record['posy'], record['posz'], record['time'])
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if result else None

    def put_ctrl(self, record):
        query = '''INSERT INTO `ctrl` (`rfid`, `apid`, `rssi`, `time`) VALUES
        ('{}', '{}', {}, '{}')'''.format(record['rfid'], record['apid'],
                                         record['rssi'], record['time'])
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if result else None
