#!/usr/bin/env python3

import connexion
from swagger_server import encoder
from swagger_server.config import BaseConfig

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = encoder.JSONEncoder
app.app.config.from_object(BaseConfig)
app.add_api('swagger.yaml', arguments={'title': 'Proyecto Cierzo API'})

def main():
    app.run(port=8080)


if __name__ == '__main__':
    main()
