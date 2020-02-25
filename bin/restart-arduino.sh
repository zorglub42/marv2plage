#!/bin/bash
service arduino-controller stop
ps aux | grep data-collector| grep -v grep | awk '{print $2}'| xargs kill -9
service arduino-controller start
nohup ./data-collector.py 2>&1 >/dev/null &
