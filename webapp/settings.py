# -*- coding: utf-8 -*-
"""FFBC8 Weather station webapp settings."""
# Flask-Restplus settings
FLASK_DEBUG = True  # Do not use debug mode in production
# RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'none'
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
# RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'full'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False
BIND = "0.0.0.0:5000"

API = {
    "base_url": "/api",
    "version": '1.0',
    "title": 'FFBC8 Weather station API',
    "description": 'FFBC8 Weather station API',
    "authorizations": None
    # {
    #     'basicAuth': {
    #         'type': 'basic',
    #     },
    #     'OSA Cookie': {
    #         'type': 'apiKey',
    #         'in': 'cookie',
    #         'name': 'OSAAuthToken',
    #         'description': (
    #             "<font color=red>Cookies are not supported by this "
    #             "Swagger API 2.0. But OSA Cookie works with regular "
    #             "HTTP Clients.</font>"
    #         )
    #     }
    # }
}
SENSORS = [
    {"id": "A_PRESS", "label": "pressure"},
    {"id": "TEMP", "label": "temperature"},
    {"id": "WIND_H", "label": "windheading"},
    {"id": "WIND_S", "label": "windspeed"},
    {"id": "HUM", "label": "humidity"},
    {"id": "PWR_LOAD", "label": "load"},
]

conf = {}  # pylint: disable=invalid-name
