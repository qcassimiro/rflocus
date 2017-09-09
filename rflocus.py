#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sqlite3
import sys

import flask
import flask_cors
import flask_restful


class RFLocus(flask_restful.Resource):
    def __init__(self):
        """ init shit """
        pass

    def get(self):
        return {}

    def put(self):
        return {}


def get_args():
    parser = argparse.ArgumentParser(description="Descricao curta do programa")
    parser.add_argument("-v",
                        "--verbose",
                        action='store_true',
                        help="Ajuda da opcao")
    parser.add_argument("-p",
                        "--port",
                        action='store',
                        type=int,
                        default=5000,
                        metavar="[1000-8000]",
                        help="Ajuda da opcao")
    args = vars(parser.parse_args())
    # verificar e/ou adicionar argumentos
    print(args)
    if args['port'] < 1000 or args['port'] > 8000:
        # logar erro de valor
        args = None
    args['machine'] = os.uname().machine
    return args


def main():
    args = get_args()
    if not args:
        return 1
    app = flask.Flask(__name__)
    flask_cors.CORS(app)
    api = flask_restful.Api(app)
    api.add_resource(RFLocus, '/')
    app.run(debug=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
