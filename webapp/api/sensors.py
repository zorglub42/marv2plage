# -*- coding: utf-8 -*-
# Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
"""FFBC8 weatherstation sensors API."""
import logging

from flask_restx import Resource, reqparse
from api.datamodel import (
    LAST_SENSORS_VALUES, GET_SENSOR_VALUES, SENSOR_VALUES_TREND
)
from api.restx import API
from services.sensors import SensorsService
NS = API.namespace(
    'sensors',
    description='sensors resources'
)


@NS.route('/last')
class Last(Resource):
    """Last value for all sensors API Class."""

    logger = None

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, api=None, *args, **kwargs):
        Resource.__init__(self, api, kwargs)
        self.logger = logging.getLogger(__name__)

    @API.marshal_with(LAST_SENSORS_VALUES)
    def get(self):
        """Return list of last values for all sensors."""

        sensor_svc = SensorsService()
        self.logger.info("sensors.Last.get")
        return sensor_svc.get_last()


@NS.route('/<string:sensor>/values')
@NS.expect(GET_SENSOR_VALUES)
class GetSensorValues(Resource):
    """Last sensors API Class."""

    logger = None

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, api=None, *args, **kwargs):
        Resource.__init__(self, api, kwargs)
        self.logger = logging.getLogger(__name__)

    @API.marshal_with(SENSOR_VALUES_TREND)
    def get(self, sensor):
        """Return a liste a min/max/min values for a period of time."""
        parser = reqparse.RequestParser()
        parser.add_argument("fromOffset")
        parser.add_argument("toOffset")
        parser.add_argument("groupInterval")

        args = parser.parse_args()

        self.logger.info("sensors.Values.get")
        self.logger.debug(
            "\tsensor=%s from=%s to=%s group=%s",
            sensor,
            args["fromOffset"],
            args["toOffset"],
            args["groupInterval"]

        )
        sensor_svc = SensorsService()
        return sensor_svc.get_sensor_trend(
            sensor, 
            args["fromOffset"],
            args["toOffset"],
            args["groupInterval"]
        )