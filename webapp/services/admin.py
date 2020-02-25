# Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
"""FFBC8 Webapp Administration service implementation."""
import json
import logging
import socket
import subprocess

import settings


class AdminService(object):
    """admin class."""

    def __init__(self):
        """Initialize Admin Service."""
        self.logger = logging.getLogger(__name__)

    def _send_to_arduino(self, command):
        """Send a commant to arduino and return result."""

        res = ""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect(
                (
                    settings.conf["ARDUINO"]["server"],
                    settings.conf["ARDUINO"]["port"]
                )
            )
            soc.sendall((command + "\n").encode("utf-8"))
            try:
                while True:
                    data = soc.recv(1024)
                    if not data:
                        break

                    res += data.decode("utf-8").replace("\r", "")
            except Exception:
                self.logger.exception("Error while communication with arduino")
            finally:
                soc.close()
            return res

    def load_conf(self):
        """Load config from ENV vars or config file."""
        with open('/etc/meteo/webapp-settings.json') as conf_file:
            config = json.load(conf_file)
        settings.conf = config

    def save_conf(self):
        """Save config to config file."""
        with open('/etc/meteo/webapp-settings.json', 'w') as outfile:
            json.dump(settings.conf, outfile, indent=4)

    def set_time(self, iso_date):
        """Set system time from iso date

        Arguments:
            iso_date {String} -- DateTime to set in ISO format
        """
        self.logger.info("Setting date to %s requested", iso_date)
        cmd = "{} {}".format(settings.conf["COMMANDS"]["settime"], iso_date)
        self.logger.debug(
            "Executing %s",
            cmd
            
        )
        subprocess.run(cmd.split(" "))
        return "OK"

    def execute_command(self, command):
        """Execute a command."""

        self.logger.info("%s requested", command)
        self.logger.debug(
            "Executing %s",
            settings.conf["COMMANDS"][command]
        )
        subprocess.run(settings.conf["COMMANDS"][command].split(" "))
        return "OK"

    def request_mag_calibration(self):
        """Request mag calibration to Arduino."""

        msg = self._send_to_arduino("CM")
        return {
            "status": "OK",
            "message": msg
        }

    def request_compass_support(self):
        """Request compass support to Arduino."""

        msg = self._send_to_arduino("HC")
        if "HC 1" in msg:
            return {
                "status": "OK",
                "message": "Compass supported"
            }
        else:
            return {
                "status": "KO",
                "message": "Compass not supported"
            }

    def request_find_north(self):
        """Request Arduino to find north."""

        msg = self._send_to_arduino("MS")
        return {
            "status": "OK",
            "message": msg
        }

    def _net_exists(self, nets, ssid):
        """Return true if ssid already in nets."""
        ret = False
        for net in nets:
            ret = ret or net["ssid"] == ssid
        return ret

    def get_wifi_hotspot(self):
        """
            Find wifi hotposts aurond device
            and current wifi configuration
        """

        self.load_conf()

        cmd = (
            "iwlist " + settings.conf["WIFI"]["if"] + " scan| "
            'egrep "Qual|SSID"'
        )

        data = subprocess.check_output(
            cmd,
            shell=True
        )
        data = data.decode().split('\n')[:-1]
        nets = []
        i = 0
        while i < len(data):
            qual_parts = data[i].strip().split("=")
            ratio = qual_parts[1].split(" ")
            ratio = ratio[0].split("/")
            qual = int(((float(ratio[0]) / float(ratio[1]))*100)/25)
            ssid_parts = data[i + 1].strip().split('"')
            ssid = ssid_parts[1]
            if qual > 0 and not self._net_exists(nets, ssid):
                nets.append(
                    {
                        "ssid": ssid,
                        "quality": qual
                    }
                )
            i += 2
        res = settings.conf["WIFI"].copy()
        res["networks"] = sorted(
            nets, key=lambda i: i['quality'], reverse=True
        )

        cmd = (
            "ifconfig " + settings.conf["WIFI"]["if"] + "| "
            "grep 'ether ' | "
            "awk '{print $2}'"
        )
        res["mac"] = subprocess.check_output(
            cmd,
            shell=True
        ).decode().replace("\n", "")
        return res

    def apply_wifi(self, wifi_conf):
        """Apply wifi configuration."""

        self.load_conf()
        settings.conf["WIFI"]["mode"] = wifi_conf["mode"]
        settings.conf["WIFI"]["client"] = wifi_conf["client"]
        settings.conf["WIFI"]["hotspot"] = wifi_conf["hotspot"]
        self.save_conf()
        subprocess.call(settings.conf["COMMANDS"]["setwifi"], shell=True)