#!/usr/bin/python3
# Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging.config
import math
import select
import socket
import sys
import time

import requests

import settings


def send_influx(data):
    if data == "":
        return False

    if settings.INFLUX["user"] is not None:
        auth = (settings.INFLUX["user"], settings.INFLUX["pass"])
    else:
        auth = None

    influx_url = settings.INFLUX["host"]+"/write?db="
    influx_url += settings.INFLUX["db"]
    response = requests.post(
        influx_url,
        data=data.encode("utf-8"),
        auth=auth,
        headers={
            "Content-Type": "application/x-www-form-urlencoded; " +
                            "charset=UTF-8"
        },
        verify=False)
    if response.status_code != 204:
        log_msg = "Error while storing measurment: {}"
        log_msg = log_msg.format(response.text)
        LOG.error(log_msg)
    else:
        LOG.debug("Send '%s' to influx", data)


def process_data(data):
    lines = data.replace("\r", "").split("\n")
    
    influx_command = ""
    for line in lines:
        if line:
            sensor = line.split(" ")
            if len(sensor) == 2:
                if influx_command != "":
                    influx_command += "\n"
                influx_command += sensor[0] + " "
                # if sensor[0] == "WIND_H":
                #     rad = math.radians(float(sensor[1]) % 360)
                #     v_sin = math.sin(rad)
                #     v_cos = math.cos(rad)
                #     if float(sensor[1]) > 180:
                #         influx_command += "relative=" + str(
                #             float(sensor[1]) - 360
                #         )
                #     else:
                #         influx_command += "relative=" + str(
                #             float(sensor[1])
                #         )
                #     influx_command += ",sin=" + str(v_sin)
                #     influx_command += ",cos=" + str(v_cos)
                #     influx_command += ","
                
                influx_command += "value=" + sensor[1]
                     
    send_influx(influx_command)


logging.config.fileConfig("/etc/meteo/data-collector-logging.conf")
LOG = logging.getLogger(__name__)
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (
    settings.ARDUINO_SERVER["host"],
    settings.ARDUINO_SERVER["port"]
)
LOG.info(
    'connecting to %s port %s',
    settings.ARDUINO_SERVER["host"],
    settings.ARDUINO_SERVER["port"]
)
def main():
    sock.connect(server_address)
    rec_data = ""
    while 1:
        socket_list = [sock]
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        for r_sock in read_sockets:
            time.sleep(0.1)
            #incoming message from remote server
            if r_sock == sock:
                data = r_sock.recv(4096)
                if not data:
                    LOG.error("Disconnected from server")
                    sys.exit()
                else:
                    rec_data += data.decode()
                    if rec_data[-1] == "\n":
                        try:
                            process_data(rec_data)
                        except Exception:
                            LOG.exception("Error while processing data from arduino")
                        rec_data = ""
                    else:
                        LOG.info("Data received incmplete: %s", rec_data)


if __name__ == "__main__":
    main()
