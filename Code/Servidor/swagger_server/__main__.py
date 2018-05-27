#!/usr/bin/env python3

import connexion
from swagger_server import encoder
from swagger_server.config import BaseConfig

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = encoder.JSONEncoder
app.app.config.from_object(BaseConfig)
app.add_api('swagger.yaml', arguments={'title': 'Proyecto Cierzo API'})

if BaseConfig.WEB_CORS == 'true':
    @app.app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', BaseConfig.WEB_URI)
        response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response


def main():
    app.run(port=8080)


if __name__ == '__main__':
    main()
