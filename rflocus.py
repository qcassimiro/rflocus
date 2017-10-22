#!/usr/bin/env python3


import flask
import flask_cors
import flask_restful

import database
import log
import multilateration


HOST = "0.0.0.0"
PORT = 5500
DEBUG = True
RFLOCUS_URI = "/"


class RFLResource(flask_restful.Resource):

    def __init__(self):
        self.database = database.RFLDatabase()

    def get(self):
        log.debug(flask.request)
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
        position = multilateration.estimate(references, distances)
        area = self.database.get_area(position)
        return {'posx': position[0], 'posy': position[1], 'posz': position[2], 'arid': area}

    def put(self):
        log.debug(flask.request)
        return {}


def main():
    log.start_logging()
    log.info("Starting RFLocus server")
    app = flask.Flask(__name__)
    flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})
    api = flask_restful.Api(app)
    log.info("RFLocus resource URI is %s", RFLOCUS_URI)
    api.add_resource(RFLResource, RFLOCUS_URI)
    app.run(host=HOST, port=PORT, debug=DEBUG)


if __name__ == "__main__":
    main()
