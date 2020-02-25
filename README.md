# Marv' de plage
Ce projet contient le code source developper pour réaliser une station meteo portable a partir de
* un raspberry PI Zero W
* un arduino Uno
* Un batterie LiPo
* Un "Grove LiPo Rider PRO" (tweaké)
* un capteur BMP280 (pression/temperature/humidité)
* une horloge RTC ds1380
* un kit de capteur "adafruit" anemo et girouette

# Contenu des repertoires :
* ```Arduino/Station``` contient le code a deployer sur l'arduino
* ```webapp``` contient le code de la webapp python
* ```bin``` un ensemble de scripts d'admin
* ```bin/etc``` des samples de conf

# pré-requis
Sur le raspberry :
* le bus I2C doit etre activé
* python3 dispo
* influxdb dispo
* arduino-controller dispo (https://raw.githubusercontent.com/zorglub42/serial-com/)
