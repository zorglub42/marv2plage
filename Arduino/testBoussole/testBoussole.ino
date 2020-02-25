/*
Advanced_I2C.ino
Brian R Taylor
brian.taylor@bolderflight.com

Copyright (c) 2017 Bolder Flight Systems

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, 
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#include "MPU9250.h"
#include "EEPROM.h"

#define CALIBRATION_COUNT 500
#define CAL_HEADER 42

#define deg360(a)   (((int)(a))+360)%360

// an MPU9250 object with the MPU-9250 sensor on I2C bus 0 with address 0x68
MPU9250 mpu(Wire,0x68);
int status;

typedef struct {
  float biasX;
  float biasY;
  float biasZ;
  float scaleX;
  float scaleY;
  float scaleZ;
} mag_params;

void calibrateMag(){
  mag_params params;
  uint8_t header;

  mpu.calibrateMag(CALIBRATION_COUNT);

  params.biasX = mpu.getMagBiasX_uT();
  params.biasY = mpu.getMagBiasY_uT();
  params.biasZ = mpu.getMagBiasZ_uT();

  params.scaleX = mpu.getMagScaleFactorX();
  params.scaleY = mpu.getMagScaleFactorY();
  params.scaleZ = mpu.getMagScaleFactorZ();

  header = CAL_HEADER;
  EEPROM.put(0, header);
  EEPROM.put(1, params);

}

uint8_t getMagCalibration(){
  uint8_t header;

  mag_params params;

  EEPROM.get(0, header);
  if (header == CAL_HEADER){
    // EEPROM.get(1+ 0*memOffset, biasX);
    // EEPROM.get(1+ 1*memOffset, biasY);
    // EEPROM.get(1+ 2*memOffset, biasZ);
    // EEPROM.get(1+ 3*memOffset, scaleX);
    // EEPROM.get(1+ 4*memOffset, scaleY);
    // EEPROM.get(1+ 5*memOffset, scaleZ);
    EEPROM.get(1, params);

    mpu.setMagCalX(params.biasX, params.scaleX);
    mpu.setMagCalY(params.biasY, params.scaleY);
    mpu.setMagCalZ(params.biasZ, params.scaleZ);

    return 1;
  }
  return 0;
}


void setup() {
  // serial to display data
  Serial.begin(9600);

  // start communication with IMU 
  status = mpu.begin();
  if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }

  Serial.println("Accell calibartion start");
  mpu.calibrateAccel();
  Serial.println("Calibration start");
//  mpu.calibrateMag();
   calibrateMag();
  Serial.println("Calibration ends");
  getMagCalibration();
}

void loop() {
  // read the sensor
  mpu.readSensor();

  float magX = mpu.getMagX_uT();
  float magY = mpu.getMagY_uT();
  float magZ = mpu.getMagZ_uT();

  float angle = atan2(magY, magX);
  Serial.print(deg360(angle));Serial.print(" ");


  float accelX = mpu.getAccelX_mss();
  float accelY = mpu.getAccelY_mss();
  float accelZ = mpu.getAccelZ_mss();

  float pitch = atan2 (accelY ,( sqrt ((accelX * accelX) + (accelZ * accelZ))));
  float roll = atan2(-accelX ,( sqrt((accelY * accelY) + (accelZ * accelZ))));

   // yaw from mag

   float Yh = (magY * cos(roll)) - (magZ * sin(roll));
   float Xh = (magX * cos(pitch))+(magY * sin(roll)*sin(pitch)) + (magZ * cos(roll) * sin(pitch));

  float yaw =  atan2(Yh, Xh);


    roll = roll*180/PI;
    pitch = pitch*180/PI;
    yaw = yaw*180/PI;
   Serial.println(yaw);


  // Serial.print(deg360(pitch));Serial.print(" ");
  // Serial.print(deg360(roll));Serial.print(" ");
  // Serial.print(deg360(yaw));Serial.print(" ");
  // Serial.println();

  delay(200);
}
