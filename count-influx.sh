influx -host 10.10.10.161 -database meteo < marv2plage.iql | egrep -v "count|---|name|^$"|awk '{print $2}'| awk '{s+=$0}END{print s}'
