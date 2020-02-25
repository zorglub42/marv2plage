# -*- coding: utf-8 -*-
"""FFBC8 Weather station webapp home page."""
import logging
from flask import render_template


class Home(object):
    """Webapp homepage implem."""

    logger = None

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def index(self):
        """Index of home page."""

        return render_template(
            'home_page/index.html',
            **locals()
        )
