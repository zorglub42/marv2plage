#!/bin/bash
# Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

MODE=$(cat /etc/meteo/webapp-settings.json | jq .WIFI.mode|awk -F '"' '{print$2}' )
IF=$(cat /etc/meteo/webapp-settings.json | jq .WIFI.if|awk -F '"' '{print$2}' )

function createHotspot(){
	SSID=$(cat /etc/meteo/webapp-settings.json | jq .WIFI.hotspot.ssid|awk -F '"' '{print$2}' )
	PASSPHRASE=$(cat /etc/meteo/webapp-settings.json | jq .WIFI.hotspot.passphrase|awk -F '"' '{print$2}' )
	echo "creating Hotspot with SSID=$SSID"
	cat /etc/dhcpcd.conf | egrep -v 'interface wlan0|static ip_address=192.168.42.1/24' > /tmp/$$
	mv /tmp/$$ /etc/dhcpcd.conf
	cat <<EOF >> /etc/dhcpcd.conf
interface wlan0
   static ip_address=192.168.42.1/24
EOF
	cat <<EOF > /etc/wpa_supplicant/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
EOF
	ifdown $IF
	ifup $IF



	sed -i "s/ssid=.*/ssid=$SSID/" /etc/hostapd/hostapd.conf
	sed -i "s/wpa_passphrase=.*/wpa_passphrase=$PASSPHRASE/" /etc/hostapd/hostapd.conf 

	service dnsmasq stop
	service hostapd stop	

	service dnsmasq start
	service hostapd start	

}

function connectWIFI(){
	service dnsmasq stop
	service hostapd stop
	SSID=$(cat /etc/meteo/webapp-settings.json | jq .WIFI.client.ssid|awk -F '"' '{print$2}' )
	iwlist $IF scan  | grep $SSID > /dev/null
	if [ $? -eq 0 ] ; then
		PASSPHRASE=$(cat /etc/meteo/webapp-settings.json | jq .WIFI.client.passphrase|awk -F '"' '{print$2}' )
		echo "$SSID found, trying to connectWIFI"
		cat <<EOF > /etc/wpa_supplicant/wpa_supplicant.conf
country=FR
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
        ssid="$SSID"
        psk="$PASSPHRASE"
        key_mgmt=WPA-PSK
}
EOF
		cat /etc/dhcpcd.conf | egrep -v 'interface wlan0|static ip_address=192.168.42.1/24' > /tmp/$$
		mv /tmp/$$ /etc/dhcpcd.conf

		ifdown $IF
		ifup $IF
		echo waitting for $IF to come up...
		ifconfig $IF| grep "inet " >/dev/null
		HAVE_IP=$?
		COUNT=0
		echo $HAVE_IP $COUNT
		while [ $HAVE_IP -ne 0 -a $COUNT -lt 20 ] ; do
			echo "$IF not yet up, waitting...."
			sleep 1
			COUNT=$(expr $COUNT + 1)
			ifconfig $IF| grep "inet " >/dev/null
			HAVE_IP=$?
		done
		if  [ $HAVE_IP -ne 0 ] ; then
			echo "Can't reach $SSID"
			createHotspot 
		else
			if [ "$SSID" != "zorglubNet" ] ; then
				nohup openvpn /home/pi/bin/Marv2PlageZorg.ovpn 2>&1 > /var/log/openvpn.log &
				Z_IF=tap0
			else
				Z_IF=wlan0
			fi
			COUNT=0
			ping -c 1 -W 1 -w 1 10.10.10.1 > /dev/null
			PING=$?
			while [ $PING -ne 0 -a $COUNT -lt 20 ] ; do
				echo Waitting for vpn to come up
				sleep 1
				COUNT=$(expr $COUT + 1)
				ping -c 1 -W 1 -w 1 10.10.10.1 > /dev/null
				PING=$?
			done
			if [ $PING -ne 0 ] ; then
				createHotspot
			else
				MAC=$(ifconfig wlan0| grep ether | awk '{print $2}')
				Z_IP=$(ifconfig $Z_IF | grep "inet 10.10.10"|awk '{print $2}')
				echo Connected to zorg network with ip $Z_IP
				curl "http://robert.zorglub42.lan:84/chat/bot/api/station.php?mac=$MAC&ip=$Z_IP"
				
			fi

		fi
	else
		createHotspot
	fi
}


killall openvpn
if [ "$MODE" == "client" ] ; then
	connectWIFI
else
	createHotspot
fi
