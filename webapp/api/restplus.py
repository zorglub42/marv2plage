# -*- coding: utf-8 -*-
# Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
"""Restplus library configuration and startup."""
import logging

from flask_restplus import Api

import settings

LOG = logging.getLogger(__name__)

# Settings for swagger meta API
API = Api(
    version=settings.API["version"],
    title=settings.API["title"],
    description=settings.API["description"],
    doc="/doc/",
    authorizations=settings.API["authorizations"]
)


@API.errorhandler
def default_error_handler(root_exception):
    """Return encountred error in REST compliant way."""
    message = 'An unhandled exception occurred.' + str(root_exception)
    LOG.exception(message)

    return {
        'status': 500,
        'message': message
    }, 500
