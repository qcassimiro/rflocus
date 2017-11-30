#!/usr/bin/env python3


import datetime
import pprint

import flask
import flask_cors
import flask_restful

import database
import log
import multilateration

HOST = "0.0.0.0"
PORT = 5500
DEBUG = False
RFLOCUS_URI = "/"


class RFLResource(flask_restful.Resource):
    def __init__(self):
        self.database = database.RFLDatabase()

    def get(self):
        now = datetime.datetime.now()
        log.debug(flask.request)
        args = dict(flask.request.args)
        if not args:
            return {}
        access_points = {}
        for k, v in args.items():
            apid = k
            rssi = float(v[0])
            rssi_tol = rssi * 0.05
            # associa todos os similares ao ap
            access_points[k] = {}
            access_points[k]['rssi'] = rssi
            access_points[k]['similar'] = self.database.get_similar(apid, rssi, rssi_tol)
        # pprint.pprint(access_points)
        references = []
        distances = []
        results = self.database.get_references(access_points.keys())
        for result in results:
            distance = 0
            reference = (result[1], result[2], result[3])
            for position in access_points[result[0]]['similar']:
                distance = distance + multilateration.euclidean(reference, position)
            distance = distance / len(access_points[result[0]]['similar'])
            # print("{}\t{}".format(result[0], distance))
            distances.append(distance)
            references.append(reference)
        position = multilateration.estimate(references, distances)
        # print("Position:\t{}".format(position))
        for apid in access_points.keys():
            record = {
                'apid': apid,
                'rssi': access_points[apid]['rssi'],
                'posx': position[0],
                'posy': position[1],
                'posz': position[2],
                'time': now.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.database.put_calc(record)
        area = self.database.get_area(position)
        return {'posx': position[0], 'posy': position[1], 'posz': position[2], 'arid': area}

    def put(self):
        now = datetime.datetime.now()
        request = flask.request.get_json(force=True)
        request_type = request.pop('type', 'none')
        measurements = request.pop('data', [])
        success = True
        if request_type in 'real':
            for measurement in measurements:
                record = {
                    'apid': measurement['apid'],
                    'rssi': measurement['rssi'],
                    'posx': measurement['posx'],
                    'posy': measurement['posy'],
                    'posz': measurement['posz'],
                    'time': now.strftime("%Y-%m-%d %H:%M:%S")
                }
                self.database.put_real(record)
        elif request_type in 'ctrl':
            for measurement in measurements:
                timestamp = now - datetime.timedelta(seconds=int(measurement['time']))
                record = {
                    'rfid': measurement['rfid'],
                    'apid': measurement['apid'],
                    'rssi': measurement['rssi'],
                    'time': timestamp.strftime("%Y-%m-%d %H:%M:%S")
                }
                self.database.put_ctrl(record)
        else:
            success = False
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
