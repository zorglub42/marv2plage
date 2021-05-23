# -*- coding: utf-8 -*-
# Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
"""FFBC8 weatherstation data model."""
from flask_restx import fields
from api.restx import API

# Model desecription for methods parameters
SYSTEM_COMMAND_PAYLOAD = API.model("systemCommand", {
    "command": fields.String(
        requied=True,
        description="Command to execute",
        enum=["shutdown", "reboot"]
    )
})
SYSTEM_TIME = API.model("dateTime", {
    "dateTime": fields.String(
        requied=True,
        description="Date is ISO format",
        example="2020-02-21T20:36:28Z"
    )
})

SENSOR_VALUE = API.model("sensorValue", {
    'name': fields.String(
        required=True,
        description='Sensor name',
        example='A_PRESS'
    ),
    'value': fields.Float(
        required=True,
        description='Sensor value',
        example=1013.78
    ),
    'timestamp': fields.Integer(
        required=True,
        description='Unix Timestamp of measurement',
        example=1556784785
    )
})
SENSOR_TREND_VALUE = API.model('sensorTrendValue', {
    "timestamp": fields.String(
        description="MEasurement timestamp in iso format",
        required=True,
        example="2019-05-02T10:15:00Z"
    ),
    "mean": fields.Float(
        description="Mean value on the period",
        required=True
    ),
    "min": fields.Float(
        description="Min value on the period",
        required=True
    ),
    "max": fields.Float(
        description="Max value on the period",
        required=True
    ),
})
SENSOR_VALUES_TREND = API.model("sensorsValueTrend", {
    "values": fields.List(
        fields.Nested(SENSOR_TREND_VALUE),
        required=False,
        description="List of values"

    )
})
LAST_SENSORS_VALUES = API.model("lastSensorsValues", {
    "pressure": fields.Nested(
        SENSOR_VALUE,
        required=False,
        description="Last value for atmospheric pressure in hPa"
    ),
    "temperature": fields.Nested(
        SENSOR_VALUE,
        required=False,
        description="Last value for temperature in °C"
    ),
    "humidity": fields.Nested(
        SENSOR_VALUE,
        required=False,
        description="Last value for humidity in %"
    ),
    "windspeed": fields.Nested(
        SENSOR_VALUE,
        required=False,
        description="Last value for wind speed in m/s"
    ),
    "windheading": fields.Nested(
        SENSOR_VALUE,
        required=False,
        description="Last value for wind heading in degrees"
    ),
    "load": fields.Nested(
        SENSOR_VALUE,
        required=False,
        description="Last value for battery load in %"
    )


})

GET_SENSOR_VALUES = API.parser()
GET_SENSOR_VALUES.add_argument(
    "fromOffset",
    type=fields.String(
        description='Offset from now for beging of period',
        example="-6h"
    ),
    required=True,

)
GET_SENSOR_VALUES.add_argument(
    "toOffset",
    type=fields.String(
        description='Offset from now for beging of period',
        example="-1m"
    ),
    required=False
)
GET_SENSOR_VALUES.add_argument(
    "groupInterval",
    type=fields.String(
        description='Regroupement interval',
        example="5m"
    ),
    required=False
)


HOTSPOT = API.model("hotspot", {
    "ssid": fields.String(
        required=True,
        description="Htospot SSID"
    ),
    "quality": fields.Integer(
        required=True,
        description='Signal quality',
        enum=[0, 1, 2, 3, 4]
    )
})
WIFI_SETTINGS = API.model("wifiSetting", {
    "ssid": fields.String(
        required=True,
        description="Wifi network SSID"
    ),
    "passphrase": fields.String(
        required=True,
        description="Wifi network passphrase"
    )
})
WIFI_CONFIG = API.model("wifiConfig", {
    "mode": fields.String(
        required=True,
        description="Nominal wifi mode",
        enum=["client", "hotspot"]
    ),
    "client": fields.List(
        fields.Nested(WIFI_SETTINGS)
    ),
    "hotspot": fields.Nested(WIFI_SETTINGS)
})
WIFI_CONFIG_EXTENDED = API.inherit("wifiConfigAdvanced", WIFI_CONFIG, {
    "networks": fields.List(fields.Nested(HOTSPOT)),
    "mac": fields.String(
        description="MAC Address"
    )
})
