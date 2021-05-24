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
	ps aux | grep openvpn|grep -v grep | awk '{print $2}' | xargs kill

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
	ifconfig $IF down
	ifconfig $IF up



	sed -i "s/ssid=.*/ssid=$SSID/" /etc/hostapd/hostapd.conf
	sed -i "s/wpa_passphrase=.*/wpa_passphrase=$PASSPHRASE/" /etc/hostapd/hostapd.conf 

	service dnsmasq stop
	service hostapd stop	

	service dnsmasq start
	service dhcpcd restart
	service hostapd start	

}

function connectWIFI(){

	service dnsmasq stop
	service hostapd stop
	SSID="" #$(cat /etc/meteo/webapp-settings.json | jq .WIFI.client[0].ssid|awk -F '"' '{print$2}' )

	iwlist $IF scan > /tmp/wifi.scan
	for KEY in $(cat /etc/meteo/webapp-settings.json | jq .WIFI.client| jq "keys"| jq -r ".[]") ; do
		echo K=$KEY
		CUR_SSID=$(cat /etc/meteo/webapp-settings.json | jq -r .WIFI.client[$KEY].ssid)
		CUR_PASSPHRASE=$(cat /etc/meteo/webapp-settings.json | jq -r .WIFI.client[$KEY].passphrase)
		grep '"'$CUR_SSID'"' /tmp/wifi.scan> /dev/null
		if [ $? -eq 0 ] ; then 
			echo "$CUR_SSID found in wifi neighbourhood"
			SSID=$CUR_SSID
			PASSPHRASE=$CUR_PASSPHRASE
			break
		fi
	done
	if [ "$SSID" != "" ] ; then
		#PASSPHRASE=$(cat /etc/meteo/webapp-settings.json | jq .WIFI.client.passphrase|awk -F '"' '{print$2}' )
		echo "Cool! $SSID was found, let's try to connectWIFI"
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

		ifconfig $IF down
		service dhcpcd restart
		ifconfig $IF up
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
			echo $HAVE_IP $COUNT
		done
		if  [ $HAVE_IP -ne 0 ] ; then
			echo "Can't reach $SSID"
			createHotspot 
		else
			if [ "$SSID" != "zorglubNet" ] ; then
				:>/var/log/openvpn.log 
				nohup openvpn /home/pi/bin/Marv2Plage.ovpn 2>&1 > /var/log/openvpn.log &
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
				COUNT=$(expr $COUNT + 1)
				ping -c 1 -W 1 -w 1 10.10.10.1 > /dev/null
				PING=$?
				echo $PING $COUNT
			done
			if [ $PING -ne 0 ] ; then
				createHotspot
			else
				MAC=$(ifconfig wlan0| grep ether | awk '{print $2}')
				Z_IP=$(ifconfig $Z_IF | grep "inet 10.10.10"|awk '{print $2}')
				echo Connected to zorg network with ip $Z_IP
				echo "curl -i http://10.10.10.22:84/chat/bot/api/station.php?mac=$MAC&ip=$Z_IP"
				curl -i "http://10.10.10.22:84/chat/bot/api/station.php?mac=$MAC&ip=$Z_IP"
				
			fi

		fi
	else
		createHotspot
	fi
}

ps aux | grep openvpn|grep -v grep | awk '{print $2}' | xargs kill

if [ "$MODE" == "client" ] ; then
	connectWIFI
else
	createHotspot
fi
ifconfig | grep tap0 > /dev/null
if [ $? -eq 0 ] ; then
        IF=tap0
else
        IF=wlan0
fi
IP=$(ifconfig $IF | grep "inet " | awk '{print $2}')
echo "IP $IP" | nc localhost 6942

exit 0
