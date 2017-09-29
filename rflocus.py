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


ACCESS_POINTS_RANGE = range(3, 10)
AREAS_RANGE = range(2, 10)
LOGGING_CONFIG_PATH = "logging.json"
PORT_DEFAULT = 5500
PORT_METAVAR = "[5000-6000]"
PORT_RANGE = range(5000, 6000)
RFLOCUS_URI = "/"
DATABASE_PATH = "rflocus.db"
DATABASE_SCRIPT_PATH = "rflocus.sql"


class RFLocus(flask_restful.Resource):

    """REST Resource class."""

    def __init__(self):
        """Implementation for the __init__ method."""
        self.database = DBWrapper(DATABASE_PATH)

    def get(self):
        """Implementation for the GET method."""
        #
        # IMPLEMENTAR ESSA PORCARIA DIREITO
        #
        # RSSI: http://127.0.0.1:5500/?type=rssi&618afa4d8e89=67&303c711fdf32=47&2cd83a4ecde3=47
        # DIST: http://127.0.0.1:5500/?type=dist&618afa4d8e89=8.48&303c711fdf32=4.47&2cd83a4ecde3=4.47
        #
        logging.debug(flask.request)
        self.database.cursor.execute("SELECT * FROM `apxy`")
        aps = self.database.cursor.fetchall()
        circles = []
        for ap in aps:
            if flask.request.args.get(ap[0]):
                circle = {}
                circle['x'] = ap[1]
                circle['y'] = ap[2]
                if flask.request.args.get('type') == "dist":
                    circle['r'] = float(flask.request.args.get(ap[0]))
                elif flask.request.args.get('type') == "rssi":
                    circle['r'] = (float(flask.request.args.get(ap[0])) - 25) / 5
                else:
                    circle['r'] = 1
                circles.append(circle)
        x = 0
        y = 0
        if len(circles) == 3:
            d1 = circles[0]['r']
            d2 = circles[1]['r']
            d3 = circles[2]['r']
            x1 = circles[0]['x']
            x2 = circles[1]['x']
            x3 = circles[2]['x']
            y1 = circles[0]['y']
            y2 = circles[1]['y']
            y3 = circles[2]['y']
            x = (((d1 ** 2 - d2 ** 2) + (x2 ** 2 - x1 ** 2) + (y2 ** 2 - y1 ** 2)) * (2 * y3 - 2 * y2) - ((d2 ** 2 - d3 ** 2) + (x3 ** 2 - x2 ** 2) + (y3 ** 2 - y2 ** 2)) * (2 * y2 - 2 * y1)) / ((2 * x2 - 2 * x3) * (2 * y2 - 2 * y1) - (2 * x1 - 2 * x2) * (2 * y3 - 2 * y2))
            y = ((d1 ** 2 - d2 ** 2) + (x2 ** 2 - x1 ** 2) + (y2 ** 2 - y1 ** 2) + x * (2 * x1 - 2 * x2)) / (2 * y2 - 2 * y1)
        self.database.cursor.execute("SELECT `arid` FROM `arxy` WHERE `minx` < {} and `maxx` > {} and `miny` < {} and `maxy` > {}".format(x, x, y, y))
        a = self.database.cursor.fetchone()
        a = a[0] if a else ""
        return {'x': x, 'y': y, 'a': a}

    def put(self):
        logging.debug(flask.request.query_string)
        """Implementation for the PUT method."""
        return {}


class DBWrapper():

    """Wrapper class for the main database."""

    def __init__(self, path=None):
        """Implementation for the __init__ method.

        Prepares main database"""
        if not os.path.exists(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
        self.__conn = sqlite3.connect(path)
        self.cursor = self.__conn.cursor()
        if not self.exists():
            self.from_script(DATABASE_SCRIPT_PATH)
        if not self.is_ready():
            raise RuntimeError("Database not ready.")

    def __exists(self, table):
        """Checks whether the specified table exists."""
        table = ''.join(c for c in table if c.isalnum())  # make query safe
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='" + table + "';"
        self.cursor.execute(query)
        return True if self.cursor.fetchall() else False

    def __count(self, table):
        """Returns the number of rows in the specified table."""
        table = ''.join(c for c in table if c.isalnum())  # make query safe
        query = "SELECT COUNT(*) FROM " + table + ";"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def __is_empty(self, table):
        """Checks if the specified table is empty."""
        return True if self.__count(table) else False

    def exists(self):
        """Checks whether the required tables exist."""
        return (self.__exists('arxy')
                and self.__exists('apxy')
                and self.__exists('real')
                and self.__exists('calc'))

    def is_ready(self):
        """Checks whether the required tables is ready."""
        return (self.__count('arxy') in AREAS_RANGE
                and self.__count('apxy') in ACCESS_POINTS_RANGE)

    def from_script(self, path):
        """Builds the main database from a SQL script."""
        if os.path.exists(path):
            query = ''
            with open(path, 'rt') as file:
                query = file.read()
            self.cursor.executescript(query)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    def __del__(self):
        """Implementation for the __del__ method."""
        self.__conn.commit()
        self.__conn.close()


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
    if not args:
        return 1
    setup_logging()
    logging.info("Starting RFLocus server")
    app = flask.Flask(__name__)
    flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})
    api = flask_restful.Api(app)
    logging.info("RFLocus resource URI is %s", (RFLOCUS_URI))
    api.add_resource(RFLocus, RFLOCUS_URI)
    app.run(host=args['host'], port=args['port'], debug=args['debug'])
    return 0


if __name__ == "__main__":
    sys.exit(main())
