# -*- coding: utf-8 -*-
# Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
"""FFBC8 Weather station webapp settings."""
# Flask-Restplus settings
FLASK_DEBUG = False  # Do not use debug mode in production
# RESTX_SWAGGER_UI_DOC_EXPANSION = 'none'
RESTX_SWAGGER_UI_DOC_EXPANSION = 'list'
# RESTX_SWAGGER_UI_DOC_EXPANSION = 'full'
RESTX_VALIDATE = False
RESTX_MASK_SWAGGER = False
RESTX_ERROR_404_HELP = False
BIND = "0.0.0.0:5000"

API = {
    "base_url": "/api",
    "version": '1.0',
    "title": 'FFBC8 Weather station API',
    "description": 'FFBC8 Weather station API',
    "authorizations": None
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
