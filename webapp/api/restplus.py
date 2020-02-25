# -*- coding: utf-8 -*-
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
