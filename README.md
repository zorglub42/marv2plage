# Marv' de plage
Ce projet contient le code source developper pour réaliser une station meteo portable a partir de
* un raspberry PI Zero W
* un arduino Uno
* Un batterie LiPo
* Un "Grove LiPo Rider PRO" (tweaké)
* un capteur BMP280 (pression/temperature/humidité)
* une horloge RTC ds1380
* un kit de capteur "adafruit" anemo et girouette

Le repertoire ```Arduino/Station``` contient le code a deployer sur l'arduino
Le repertoire ```webapp``` contient le code de la webapp python
Le repertoire ```bin``` un ensemble de scripts d'admin
Le repetroire ```bin/etc``` des samples de conf

# pré-requis
Sur le raspberry :
* le bus I2C doit etre activé
* python3 dispo
* influxdb dispo
* arduino-controller dispo (https://raw.githubusercontent.com/zorglub42/serial-com/)
