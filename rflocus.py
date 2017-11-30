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
            # para cada (mac, rssi):
            # faz um range toleravel em torno de rssi - 5-10%
            # sigst = float(v[0]) #
            # D = sigst * 0.1 #
            # selecionar todas as coordenadas em 'real' onde rssi_b esta no range
            # SELECT posx, posy, posz, rssi from real WHERE rssi BETWEEN sigst - D AND sigst + D #
            # para cada coordenada selecionada calcular uma distancia ate o ap
            # for result in results:
            #     dist = euclidean(result, posap)
            # para cada distancia montar tupla (distancia, rssi, rssi_b)
            # fazer uma media ponderada das distancias nas tuplas, com base em rssi - rssi_b
            # retornar distancia
            # colocar todas as distancias retornadas em access_points[k]
            access_points[k] = float(v[0]) * 1.0
        results = self.database.get_references(access_points.keys())
        references = []
        distances = []
        for result in results:
            distances.append(access_points[result[0]])
            references.append([result[1], result[2], result[3]])
        position = multilateration.estimate(references, distances)
        for apid in access_points.keys():
            record = {
                'apid': apid,
                'rssi': access_points[apid],
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
