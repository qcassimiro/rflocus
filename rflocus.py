#!/usr/bin/env python3

import argparse
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

import config


class RFLocus(flask_restful.Resource):

    def __init__(self):
        self.conn = sqlite3.connect(config.DATABASE)
        self.curs = self.conn.cursor()
        # logging.debug(pprint.pformat(args))

    def get(self):
        logging.debug(flask.request.query_string)
        a = flask.request.args.get('a')
        logging.debug('a is {} of type {}'.format(a, type(a)))
        b = flask.request.args.get('b')
        logging.debug('b is {} of type {}'.format(b, type(b)))
        return {}

    def put(self):
        return {}

    def __del__(self):
        self.conn.close()


def setup_arguments():
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
                        default=config.PORT_DEFAULT,
                        metavar=config.PORT_METAVAR,
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
    if args['port'] not in config.PORT_RANGE:
        error = "Invalid port number: {}".format(args['port'])
        args = None
    else:
        pass
    if error:
        print()
        print(error)
        print()
        parser.print_help()
    return args


def setup_logging(config_path=config.LOGCONF, level=logging.INFO):
    if os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)


def setup_database(db_path=config.DATABASE):
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute(config.EXISTS_ARXY)
    nareas = len(curs.fetchall())
    if nareas not in config.NAREAS_RANGE:
        conn.close()
        message = "Incompatible number of areas detected: {}".format(nareas)
        raise Exception(message)  # TODO: raise custom exception
    curs.execute(config.EXISTS_APXY)
    naps = len(curs.fetchall())
    if naps not in config.NAPS_RANGE:
        conn.close()
        message = "Incompatible number of access points detected: {}".format(naps)
        raise Exception(message)  # TODO: raise custom exception
    curs.execute(config.EXISTS_REAL)
    if not len(curs.fetchall()):
        curs.execute(config.CREATE_REAL)
        logging.warn("Table of measured values table didn't exist and was created.")
    curs.execute(config.EXISTS_CALC)
    if not len(curs.fetchall()):
        curs.execute(config.CREATE_CALC)
        logging.warn("Table of calculated values table didn't exist and was created.")
    conn.close()


def main():
    args = setup_arguments()
    if not args:
        return 1
    setup_logging()
    try:
        setup_database()
    except:
        logging.exception("RFLocus wasn't able to set the database.")
        return 1
    '''
    logging.info("Starting RFLocus server")
    app = flask.Flask(__name__)
    flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})
    api = flask_restful.Api(app)
    logging.info("RFLocus resource URI is {}".format(config.RFLOCUS_URI))
    api.add_resource(RFLocus, config.RFLOCUS_URI)
    app.run(host=args['host'], port=args['port'], debug=args['debug'])
    '''
    return 0


if __name__ == "__main__":
    sys.exit(main())
