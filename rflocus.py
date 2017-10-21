#!/usr/bin/env python3

"""
Module docstring nonsense
"""

import argparse
import errno
import json
import logging
import logging.config
import os
import platform
import sqlite3
import sys

import flask
import flask_cors
import flask_restful

import multilateration


ACCESS_POINTS_RANGE = range(3, 10)
AREAS_RANGE = range(2, 10)
LOGGING_CONFIG_PATH = "logging.json"
PORT_DEFAULT = 5500
PORT_METAVAR = "[5000-6000]"
PORT_RANGE = range(5000, 6000)
RFLOCUS_URI = "/"
DATABASE_PATH = "rflocus.db"
DATABASE_BUILD_PATH = "rflocusb.sql"
DATABASE_POPULATE_PATH = "rflocusp.sql"


class RFLResource(flask_restful.Resource):

    """REST Resource class."""

    def __init__(self):
        """Implementation for the __init__ method."""
        self.database = RFLDatabase(DATABASE_PATH)

    def get(self):
        """Implementation for the GET method."""
        logging.debug(flask.request)
        args = dict(flask.request.args)
        if not args:
            return {}
        req_type = args.pop('type', None)[0]
        if not args:
            return {}
        req_aps = {k: float(v[0]) for k, v in args.items()}
        # rssi to distance
        aps = {}
        if 'rssi' in req_type:
            for k, v in req_type.items():
                aps[k] = v / 2  # estimate distance for rssi of v
        else:
            aps = req_aps
        #
        refs = self.database.get_references(tuple(aps.keys()))
        references = []
        distances = []
        for ref in refs:
            distances.append(aps[ref[0]])
            references.append([ref[1], ref[2], ref[3]])
        print(distances)
        print(references)
        position = multilateration.estimate(references, distances)
        area = self.database.get_area(position)
        print(area)
        return {'posx': position[0], 'posy': position[1], 'posz': position[2], 'arid': area}

    def put(self):
        logging.debug(flask.request)
        """Implementation for the PUT method."""
        return {}


class RFLDatabase():

    """Wrapper class for the main database."""

    def __init__(self, path=None):
        """Implementation for the __init__ method.
        Prepares main database"""
        if not os.path.exists(path):
            # raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
            open(path, 'w').close()
        self.__conn = sqlite3.connect(path)
        self.__curs = self.__conn.cursor()
        if not self.__built():
            self.__from_script(DATABASE_BUILD_PATH)
        if not self.__is_ready():
            # raise RuntimeError("Database not ready.")
            self.__from_script(DATABASE_POPULATE_PATH)

    def __exists(self, table):
        """Checks whether the specified table exists."""
        table = ''.join(c for c in table if c.isalnum())
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='" + table + "';"
        self.__curs.execute(query)
        return True if self.__curs.fetchall() else False

    def __count(self, table):
        """Returns the number of rows in the specified table."""
        table = ''.join(c for c in table if c.isalnum())
        query = "SELECT COUNT(*) FROM `" + table + "`;"
        self.__curs.execute(query)
        return self.__curs.fetchone()[0]

    def __is_empty(self, table):
        """Checks if the specified table is empty."""
        return True if self.__count(table) else False

    def __built(self):
        """Checks whether the required tables exist."""
        return (self.__exists('arxyz')
                and self.__exists('apxyz')
                and self.__exists('real')
                and self.__exists('calc'))

    def __is_ready(self):
        """Checks whether the required tables is ready."""
        return (self.__count('arxyz') in AREAS_RANGE
                and self.__count('apxyz') in ACCESS_POINTS_RANGE)

    def __from_script(self, path):
        """Builds the main database from a SQL script."""
        if os.path.exists(path):
            query = ''
            with open(path, 'rt') as file:
                query = file.read()
            self.__curs.executescript(query)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    def __del__(self):
        """Implementation for the __del__ method."""
        self.__conn.commit()
        self.__conn.close()

    def get_references(self, apids):
        apids = str(tuple([''.join(c for c in apid if c.isalnum()) for apid in apids]))
        query = "SELECT * FROM `apxyz` WHERE `apid` IN " + apids + ";"
        self.__curs.execute(query)
        return self.__curs.fetchall()

    def get_area(self, posxyz):
        x = posxyz[0]
        y = posxyz[1]
        z = posxyz[2]
        if type(x) is not int or type(y) is not int or type(z) is not int:
            return None
        query = "SELECT `arid` FROM `arxyz` WHERE `minx` < {} and `maxx` > {} and `miny` < {} and `maxy` > {} and `minz` < {} and `maxz` > {}".format(x, x, y, y, z, z)
        self.__curs.execute(query)
        return self.__curs.fetchone()[0]


def setup_arguments():
    """Checks the arguments passed in the command line."""
    parser = argparse.ArgumentParser(description='''
        Descricao curta do programa
        ''')
    parser.add_argument("-v",
                        "--verbose",
                        action='store_true',
                        help="Ajuda da opcao")
    parser.add_argument("-p",
                        "--port",
                        action='store',
                        type=int,
                        default=PORT_DEFAULT,
                        metavar=PORT_METAVAR,
                        help="Ajuda da opcao")
    args = vars(parser.parse_args())  # 'dictfy' arguments
    args['host'] = '0.0.0.0'  # TODO: add to command line
    args['debug'] = True  # TODO: add to command line
    args['system'] = platform.system()
    args['machine'] = platform.machine()
    args['plaform'] = platform.platform()
    args['processor'] = platform.processor()
    # validate arguments
    error = None
    if args['port'] not in PORT_RANGE:
        error = "Invalid port number: {}.".format(args['port'])
        args = None
    else:
        pass
    if error:
        print()
        print(error)
        print()
        parser.print_help()
    return args


def setup_logging(config_path=LOGGING_CONFIG_PATH, level=logging.INFO):
    """Sets the logging configuration from a file."""
    if os.path.exists(config_path):
        with open(config_path, 'rt') as file:
            config = json.load(file)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)


def main():
    """Implementation for the 'main' function."""
    args = setup_arguments()
    setup_logging()
    logging.info("Starting RFLocus server")
    app = flask.Flask(__name__)
    flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})
    api = flask_restful.Api(app)
    logging.info("RFLocus resource URI is %s", (RFLOCUS_URI))
    api.add_resource(RFLResource, RFLOCUS_URI)
    app.run(host=args['host'], port=args['port'], debug=args['debug'])
    return 0


if __name__ == "__main__":
    sys.exit(main())
