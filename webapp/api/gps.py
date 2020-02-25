# -*- coding: utf-8 -*-
"""FFBC8 weatherstation receive GPS data."""
import logging

from flask import request
from flask_restplus import Resource
import requests
from api.restplus import API

import settings
NS = API.namespace(
    'GPS',
    description='receive GPS data'
)


@NS.route('/')
class GPS(Resource):
    """Receive GPS data API Class."""

    logger = None

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, api=None, *args, **kwargs):
        Resource.__init__(self, api, kwargs)
        self.logger = logging.getLogger(__name__)

    def _send_influx(self, data):
        if data == "":
            return False

        if settings.conf["INFLUX"]["user"] is not None:
            auth = (
                settings.conf["INFLUX"]["user"],
                settings.conf["INFLUX"]["pass"])
        else:
            auth = None

        influx_url = settings.conf["INFLUX"]["host"]+"/write?db="
        influx_url += settings.conf["INFLUX"]["db"]
        response = requests.post(
            influx_url,
            data=data.encode("utf-8"),
            auth=auth,
            headers={
                "Content-Type": "application/x-www-form-urlencoded; " +
                                "charset=UTF-8"
            },
            verify=False)
        if response.status_code != 204:
            log_msg = "Error while storing measurment: {}"
            log_msg = log_msg.format(response.text)
            self.logger.error(log_msg)

    def post(self):
        """Return list of last values for all sensors."""

        data = request.json
        self.logger.debug("\t%s", data)
        spd = data["speed"]
        if spd is None:
            spd = "0"
        else:
            spd = str(spd)
        influx_data = "GPS_S value=" + spd + " " + str(data["timestamp"]*1000000)
        self.logger.debug(influx_data)
        self._send_influx(influx_data)
        return "OK"
