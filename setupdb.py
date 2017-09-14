#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sqlite3
import sys

import logging.config

import config


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


def main():
    args = setup_arguments()
    if not args:
        return 1
    setup_logging()
    conn = sqlite3.connect(config.DATABASE)
    curs = conn.cursor()
    curs.execute(config.EXISTS_ARXY)
    exists_arxy = len(curs.fetchall())
    if not exists_arxy:
        curs.execute(config.CREATE_ARXY)
    curs.execute(config.ISEMPTY_ARXY)
    nareas = len(curs.fetchall())
    if nareas not in config.NAREAS_RANGE:
        # REGISTER AREAS
        pass
    curs.execute(config.EXISTS_APXY)
    exists_apxy = len(curs.fetchall())
    if not exists_apxy:
        curs.execute(config.CREATE_APXY)
    curs.execute(config.ISEMPTY_APXY)
    naps = len(curs.fetchall())
    if naps not in config.NAPS_RANGE:
        # REGISTER ACCESS POINTS
        pass
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
