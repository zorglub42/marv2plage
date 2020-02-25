# -*- coding: utf-8 -*-
"""FFBC8 Weather station webapp."""
import logging.config

# from flask import Flask, render_template, url_for
import flask_restplus.apidoc
from flask import Blueprint, Flask

from api.restplus import API as api
from api.admin import NS as admin_ns
from api.sensors import NS as sensors_ns
from api.phone import NS as phone_ns
from pages.home import Home
from services.admin import AdminService
import settings

APP = Flask(__name__)
logging.config.fileConfig('/etc/meteo/webapp-logging.conf')
LOG = logging.getLogger(__name__)


class ProxyFix(object):

    """This middleware can be applied to add HTTP proxy support to an
    application that was not designed with HTTP proxies in mind.  It
    sets `REMOTE_ADDR`, `HTTP_HOST` from `X-Forwarded` headers.  While
    Werkzeug-based applications already can use
    :py:func:`werkzeug.wsgi.get_host` to retrieve the current host even if
    behind proxy setups, this middleware can be used for applications which
    access the WSGI environment directly.

    If you have more than one proxy server in front of your app, set
    `num_proxies` accordingly.

    Do not use this middleware in non-proxy setups for security reasons.

    The original values of `REMOTE_ADDR` and `HTTP_HOST` are stored in
    the WSGI environment as `werkzeug.proxy_fix.orig_remote_addr` and
    `werkzeug.proxy_fix.orig_http_host`.

    :param app: the WSGI application
    :param num_proxies: the number of proxy servers in front of the app.
    """

    def __init__(self, app, num_proxies=1):
        self.app = app
        self.num_proxies = num_proxies

    def get_remote_addr(self, forwarded_for):
        """Selects the new remote addr from the given list of ips in
        X-Forwarded-For.  By default it picks the one that the `num_proxies`
        proxy server provides.  Before 0.9 it would always pick the first.

        .. versionadded:: 0.8
        """
        if len(forwarded_for) >= self.num_proxies:
            return forwarded_for[self.num_proxies-1]
        return None

    def get_remote_host(self, forwarded_host):
        """Selects the new remote host from the given list of hosts in
        X-Forwarded-Host.  By default it picks the one that the `num_proxies`
        proxy server provides.

        """
        if len(forwarded_host) >= self.num_proxies:
            return forwarded_host[self.num_proxies-1]
        return None

    def get_remote_proto(self, forwarded_proto):
        """Selects the new remote proto from the given list of proto in
        X-Forwarded-Proto.  By default it picks the one that the `num_proxies`
        proxy server provides.

        """
        if len(forwarded_proto) >= self.num_proxies:
            return forwarded_proto[self.num_proxies-1]
        return None

    def __call__(self, environ, start_response):
        getter = environ.get
        forwarded_proto = getter('HTTP_X_FORWARDED_PROTO', '').split(',')
        forwarded_for = getter('HTTP_X_FORWARDED_FOR', '').split(',')
        forwarded_host = getter('HTTP_X_FORWARDED_HOST', '').split(',')
        environ.update({
            'werkzeug.proxy_fix.orig_wsgi_url_scheme':
                getter('wsgi.url_scheme'),
            'werkzeug.proxy_fix.orig_remote_addr':
                getter('REMOTE_ADDR'),
            'werkzeug.proxy_fix.orig_http_host':
                getter('HTTP_HOST')
        })
        forwarded_for = [x for x in [x.strip() for x in forwarded_for] if x]
        forwarded_host = [x for x in [x.strip() for x in forwarded_host] if x]
        forwarded_proto = [x for x in [x.strip() for x in forwarded_proto] if x]

        remote_addr = self.get_remote_addr(forwarded_for)
        if remote_addr is not None:
            environ['REMOTE_ADDR'] = remote_addr
        if forwarded_host:
            environ['HTTP_HOST'] = self.get_remote_host(forwarded_host)
        if forwarded_proto:
            environ['wsgi.url_scheme'] = self.get_remote_proto(
                forwarded_proto
            )
        return self.app(environ, start_response)


def configure_app(flask_app):
    """Load application configuration to flask.

    Load configuration to Flask object
        :param flask_app: Flask application to configure
        :type flask_app: Flask
    """
    flask_app.config[
        'SWAGGER_UI_DOC_EXPANSION'
    ] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION

    flask_app.config[
        'RESTPLUS_VALIDATE'
    ] = settings.RESTPLUS_VALIDATE

    flask_app.config[
        'RESTPLUS_MASK_SWAGGER'
    ] = settings.RESTPLUS_MASK_SWAGGER

    flask_app.config[
        'ERROR_404_HELP'
    ] = settings.RESTPLUS_ERROR_404_HELP

    flask_app.config[
        'APPLICATION_ROOT'
    ] = settings.API["base_url"]


def initialize_app(flask_app):
    """Apply application configuration.

    Load configuration to Flask object and apply configuration to it
        :param flask_app: Flask application to configure
        :type flask_app: Flask
    """
    configure_app(flask_app)

    # Fix to handle properly X-Forwarded-Proto header
    # from werkzeug.contrib.fixers import ProxyFix
    flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)

    # Define base_url for the app
    blueprint = Blueprint(
        'api', __name__,
        url_prefix=settings.API["base_url"]
    )
    api.init_app(blueprint)
    api.add_namespace(admin_ns)
    api.add_namespace(sensors_ns)
    api.add_namespace(phone_ns)

    # Define base_url from swaggerui resources (js, css...)
    api_doc = flask_restplus.apidoc.apidoc
    api_doc.url_prefix = settings.API["base_url"] + "/doc"

    flask_app.register_blueprint(blueprint)


@APP.after_request
def after_request(response):
    """Add CORS Headers."""

    if response.content_type == "application/json":
        response.headers.add(
            'Access-Control-Allow-Origin',
            '*'
        )
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE'
        )
        response.headers.add(
            'Expires',
            'Sat, 26 Jul 1997 05:00:00 GMT'
        )
        response.headers.add(
            'Cache-Control',
            'no-store, no-cache, must-revalidate, max-age=0'
        )
        response.headers.add(
            'Cache-Control',
            'post-check=0, pre-check=0'
        )
        response.headers.add(
            'Pragma',
            'no-cache'
        )
    return response


def main():
    """Application launcher."""
    server_binding = settings.BIND.split(':')
    APP.run(debug=settings.FLASK_DEBUG,
            port=int(server_binding[1]),
            host=server_binding[0],
            threaded=True)


def load_config():
    """Load application config from YAML and init."""
    admin_svc = AdminService()
    admin_svc.load_conf()
    initialize_app(APP)
    LOG.info('>>>>> Starting server  <<<<<')


@APP.route('/', methods=['GET', 'POST'])
def home_index():
    """Application home page."""
    home = Home()

    return home.index()


load_config()
if __name__ == "__main__":
    main()


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)
