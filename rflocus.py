#!/usr/bin/env python3

import argparse
import errno
import json
import logging
import os
import platform
import pprint
import sqlite3
import sys

import logging.config

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
        logging.debug(flask.request.query_string)
        a = flask.request.args.get('a')
        logging.debug('a is {} of type {}'.format(a, type(a)))
        b = flask.request.args.get('b')
        logging.debug('b is {} of type {}'.format(b, type(b)))
        return {}

    def put(self):
        """Implementation for the PUT method."""
        return {}


class DBWrapper():

    """Wrapper class for the main database."""

    def __init__(self, path=None):
        """Implementation for the __init__ method.

        Prepares main database"""
        self.__conn = None
        if not path:
            raise ValueError("Path to database not specified.")
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
        """Returns the number of rows in thespecified table."""
        table = ''.join(c for c in table if c.isalnum())  # make query safe
        query = "SELECT COUNT(*) FROM " + table + ";"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def __is_empty(self, table):
        """Checks if the specified table is empty."""
        return True if self.count(table) else False

    def exists(self):
        """Checks whether the required tables exist."""
        return self.__exists('arxy') and self.__exists('apxy') and self.__exists('real') and self.__exists('calc')

    def is_ready(self):
        """Checks whether the required tables is ready."""
        return self.__count('arxy') in AREAS_RANGE and self.__count('arxy') not in ACCESS_POINTS_RANGE

    def from_script(self, path):
        """Builds the main database from a SQL script."""
        if os.path.exists(path):
            query = ''
            with open(path, 'rt') as f:
                query = f.read()
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
        with open(config_path, 'rt') as f:
            config = json.load(f)
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
    logging.info("RFLocus resource URI is {}".format(RFLOCUS_URI))
    api.add_resource(RFLocus, RFLOCUS_URI)
    app.run(host=args['host'], port=args['port'], debug=args['debug'])
    return 0


if __name__ == "__main__":
    sys.exit(main())
