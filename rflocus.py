#!/usr/bin/env python3

import argparse
import json
import logging
import os
import platform
import sqlite3
import sys
import yaml

import logging.config

import flask
import flask_cors
import flask_restful


class RFLocus(flask_restful.Resource):

    def __init__(self):
        pass

    def get(self):
        return {}

    def put(self):
        return {}


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
                        default=5000,
                        metavar="[5000-5500]",
                        help="Ajuda da opcao")
    # - parse args into a dict
    args = vars(parser.parse_args())
    # - add system arguments
    #   - running on raspberry?
    args['machine'] = platform.machine()
    args['plaform'] = platform.platform()
    # - check arguments (elif chain preferred for flow consistency)
    if args['port'] < 5000 or args['port'] > 5500:
        print("Out of bounds")
        args = None
    else:
        pass
    return args


def setup_logging(config_path='logging.yaml', level=logging.INFO):
    if os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)


def main():
    args = setup_arguments()
    if not args:
        return 1
    setup_logging()
    logging.info("Starting RFLocus server...")
    app = flask.Flask(__name__)
    flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})
    api = flask_restful.Api(app)
    logging.info("RFLocus resource URI is '/'")
    api.add_resource(RFLocus, '/')
    app.run(debug=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
