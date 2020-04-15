#!/bin/bash
# Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

service arduino-controller stop
ps aux | grep data-collector| grep -v grep | awk '{print $2}'| xargs kill -9
service arduino-controller start
/home/pi/bin/start-data-collector
