# -*- coding: utf-8 -*-
# Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
"""FFBC8 weatherstation receive phone/browser data."""
import logging
import socket
import subprocess

from flask import request
from flask_restx import Resource
import requests
from api.restx import API

import settings
NS = API.namespace(
    'phone',
    description='interact with phone'
)


@NS.route('/GPS')
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
        """Receive GPS data."""

        data = request.json
        self.logger.debug("\t%s", data)
        spd = data["speed"]
        if spd is None:
            spd = "0"
        else:
            spd = str(spd)
        influx_data = "GPS_S value=" + spd
        self.logger.debug(influx_data)
        self._send_influx(influx_data)
        return "OK"


@NS.route('/time')
class Time(Resource):
    """Receive date time from phone API Class."""

    logger = None

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, api=None, *args, **kwargs):
        Resource.__init__(self, api, kwargs)
        self.logger = logging.getLogger(__name__)

    def post(self):
        """Receive datetime from phone and set RPI datetime."""

        data = request.json
        self.logger.debug("\t%s", data)

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect the socket to the port where the server is listening
            cmd = "ST " + data["timestamp"] + "\n"
            server_address = (
                settings.conf["ARDUINO"]["server"],
                settings.conf["ARDUINO"]["port"]
            )
            sock.connect(server_address)
            sock.sendall(cmd.encode("utf-8"))
            sock.close()
            subprocess.run(
                (
                    settings.conf["COMMANDS"]["settime"] + " " + data["timestamp"]
                ).split(" ")
            )

        except Exception:  # pylint: disable=broad-except
            self.logger.exception("Error while connecting arduino")
        return "OK"
