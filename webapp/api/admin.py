# -*- coding: utf-8 -*-
# Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
"""FFBC8 weatherstation Admin API."""
import logging

from flask import request
from flask_restplus import Resource

from api.datamodel import SYSTEM_COMMAND_PAYLOAD, SYSTEM_TIME,\
    WIFI_CONFIG_EXTENDED, WIFI_CONFIG
from api.restplus import API
from services.admin import AdminService

NS = API.namespace(
    'admin',
    description='Weather station admin'
)


@NS.route("/ping")
class Pinger(Resource):
    """System pingers."""

    logger = None

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, api=None, *args, **kwargs):
        Resource.__init__(self, api, kwargs)
        self.logger = logging.getLogger(__name__)

    def get(self):
        """Ping system."""
        return "OK"


@NS.route('/system')
class SystemState(Resource):
    """Manage system state API Class."""

    logger = None

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, api=None, *args, **kwargs):
        Resource.__init__(self, api, kwargs)
        self.logger = logging.getLogger(__name__)

    @NS.expect(SYSTEM_COMMAND_PAYLOAD)
    def post(self):
        """Receive System state."""

        data = request.json
        self.logger.debug("\t%s", data)

        admin_svc = AdminService()
        admin_svc.execute_command(data["command"])
        return "OK"

@NS.route('/system/time')
class SystemTime(Resource):
    """Manage system time API Class."""

    logger = None

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, api=None, *args, **kwargs):
        Resource.__init__(self, api, kwargs)
        self.logger = logging.getLogger(__name__)

    @NS.expect(SYSTEM_TIME)
    def post(self):
        """Receive System time."""

        data = request.json
        self.logger.debug("\t%s", data)

        admin_svc = AdminService()
        admin_svc.set_time(data["dateTime"])
        return "OK"


@NS.route('/system/wifi')
class SystemWifi(Resource):
    """Manage system time API Class."""

    logger = None

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, api=None, *args, **kwargs):
        Resource.__init__(self, api, kwargs)
        self.logger = logging.getLogger(__name__)

    @NS.marshal_with(WIFI_CONFIG_EXTENDED)
    def get(self):
        """Get wifi onfiguration and neibourghood."""

        admin_svc = AdminService()
        return admin_svc.get_wifi_hotspot()

    @NS.expect(WIFI_CONFIG)
    def post(self):
        """Apply wifi settings."""

        admin_svc = AdminService()
        admin_svc.apply_wifi(request.json)
        return "OK"

@NS.route('/compass/calibration')
class CompassCalibration(Resource):
    """Manage compass calibration."""

    logger = None

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, api=None, *args, **kwargs):
        Resource.__init__(self, api, kwargs)
        self.logger = logging.getLogger(__name__)

    def post(self):
        """Request mag compass calibration to arduino."""

        admin_svc = AdminService()
        return admin_svc.request_mag_calibration()


@NS.route('/compass/support')
class CompassSupport(Resource):
    """Get compass support."""

    logger = None

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, api=None, *args, **kwargs):
        Resource.__init__(self, api, kwargs)
        self.logger = logging.getLogger(__name__)

    def get(self):
        """Request compass support to arduino."""

        admin_svc = AdminService()
        return admin_svc.request_compass_support()


@NS.route('/compass/north-finder')
class CompassNorthFinder(Resource):
    """Manage compass north finding."""

    logger = None

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, api=None, *args, **kwargs):
        Resource.__init__(self, api, kwargs)
        self.logger = logging.getLogger(__name__)

    def post(self):
        """Request arduino to find magnetic north."""

        admin_svc = AdminService()
        return admin_svc.request_find_north()
