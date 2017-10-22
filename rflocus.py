#!/usr/bin/env python3


import datetime

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
        access_points = {}
        for k, v in args.items():
            access_points[k] = float(v[0]) * 1.0  # estimate distance for rssi of v
        results = self.database.get_references(tuple(access_points.keys()))
        references = []
        distances = []
        for result in results:
            distances.append(access_points[result[0]])
            references.append([result[1], result[2], result[3]])
        position = multilateration.estimate(references, distances)
        for apid in access_points.keys():
            record = {}
            record['apid'] = apid
            record['rssi'] = access_points[apid]
            record['posx'] = position[0]
            record['posy'] = position[1]
            record['posz'] = position[2]
            record['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            self.database.put_record('calc', record)
        area = self.database.get_area(position)
        return {'posx': position[0], 'posy': position[1], 'posz': position[2], 'arid': area}

    def put(self):
        access_points = flask.request.get_json(force=True)
        success = True
        for apid in access_points.keys():
            record = {}
            record['apid'] = apid
            record['rssi'] = access_points[apid]['rssi']
            record['posx'] = access_points[apid]['posx']
            record['posy'] = access_points[apid]['posy']
            record['posz'] = access_points[apid]['posz']
            record['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            self.database.put_record('real', record)
        return {'success': success}


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
