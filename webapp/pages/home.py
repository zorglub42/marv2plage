# -*- coding: utf-8 -*-
# Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
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
