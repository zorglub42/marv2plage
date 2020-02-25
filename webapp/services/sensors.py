# Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
"""FFBC8 Webapp Sensors service implementation."""
import dateutil.parser
import datetime
import json
import logging
import urllib

import requests

import settings


class SensorsService(object):
    """Sensors class."""

    def __init__(self):
        """Initialize Sensors Service."""
        self.logger = logging.getLogger(__name__)

    def _get_last_measurement(self, sensor):
        
        """Get last measurment for a particular sensor."""

        res = None
        if settings.conf["INFLUX"]["user"] is not None:
            auth = (
                settings.conf["INFLUX"]["user"], 
                settings.conf["INFLUX"]["pass"]
            )
        else:
            auth = None

        str_select = "SELECT last(value) FROM " + sensor
        influx_url = settings.conf["INFLUX"]["host"] + "/query?q="
        influx_url += urllib.parse.quote(str_select)
        influx_url += "&db=" + urllib.parse.quote(
            settings.conf["INFLUX"]["db"]
        )
        response = requests.get(influx_url, auth=auth, verify=False)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            if "series" in json_data["results"][0]:
                data = json_data["results"][0]["series"][0]
                
                data_dt = dateutil.parser.parse(data["values"][0][0])
                res = {
                    "name": data["name"],
                    "value": data["values"][0][1],
                    "timestamp": int(data_dt.timestamp())
                }

        return res

    def get_last(self):
        """Return last sensors values"""
        res = {}
        for sens in settings.SENSORS:
            res[sens["label"]] = self._get_last_measurement(sens["id"])

        return res

    def get_sensor_trend(
        self, sensor, from_offset, to_offset=None, group_interval="5m"
    ):
        """Return a list a tren values for this sensor."""
        res = {
            "values": []
        }

        if settings.conf["INFLUX"]["user"] is not None:
            auth = (
                settings.conf["INFLUX"]["user"],
                settings.conf["INFLUX"]["pass"]
            )
        else:
            auth = None

        if group_interval is None:
            group_interval = "5m"

        from_offset = from_offset.replace("-", " - ")
        str_time_clause = "time >= now()" + from_offset + " "
        if to_offset is not None and to_offset != "":
            to_offset = to_offset.replace("-", " - ")
            str_time_clause += " AND time <= now()" + to_offset
        # SELECT atan2(mean(sin),mean(cos))*57.2958 from WIND_H
        if sensor == "WIND_H":
            # compute avg orientation from avg cos and sin in deg 
            cols = "(min(relative)+360)%360, "
            cols += "(max(relative)+360)%360, "
            cols += "(360+(atan2(mean(sin),mean(cos))*57.2958))%360"

            str_from = ""
            # Compute relative, sin and cos of stored direction
            str_from += "SELECT atan2(sin(value), " 
            str_from += "       cos(value))*57.29580406904963 as relative, "
            str_from += "       sin(value) as sin, cos(value) as cos "
            str_from += "FROM ("
            # convert stored directions form deg to rad
            str_from += "       SELECT  time, "
            str_from += "               (value%360)*0.0174533 as value "
            str_from += "       FROM WIND_H "
            str_from += "       WHERE " + str_time_clause
            str_from += ")"
            str_from = "(" + str_from + ")"
        else:
            cols = "min(value), max(value), mean(value)"
            str_from = sensor
        
        self.logger.debug(str_from)
        str_select = "SELECT " + cols + " "
        str_select += "FROM " + str_from + " "
        str_select += "WHERE " + str_time_clause
        str_select += " GROUP BY time(" + group_interval + ") fill(linear)"
        self.logger.debug(str_select)

        influx_url = settings.conf["INFLUX"]["host"] + "/query?q="
        influx_url += urllib.parse.quote(str_select)
        influx_url += "&db=" + urllib.parse.quote(
            settings.conf["INFLUX"]["db"]
        )
        response = requests.get(influx_url, auth=auth, verify=False)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            if "series" in json_data["results"][0]:
                values = json_data["results"][0]["series"][0]["values"]
                for value in values:
                    res["values"].append(
                        {
                            "timestamp": value[0],
                            "min": value[1],
                            "max": value[2],
                            "mean": value[3]
                        }
                    )
            else:
                return None, 404
        return res
