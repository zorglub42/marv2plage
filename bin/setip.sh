ifconfig | grep tap0 > /dev/null
if [ $? -eq 0 ] ; then
        IF=tap0
else
        IF=wlan0
fi
IP=$(ifconfig $IF | grep "inet " | awk '{print $2}')
echo "IP $IP" | nc localhost 6942

