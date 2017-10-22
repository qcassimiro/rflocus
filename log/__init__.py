#!/usr/bin/python3


import json
import logging
import logging.config
import os


CONFIG = "log/config.json"

debug = logging.debug
info = logging.info
warning = logging.warning


def start_logging(level=logging.INFO):
    if os.path.exists(CONFIG):
        with open(CONFIG, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)
