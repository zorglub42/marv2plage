// Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Apache License, Version 2.0
// which accompanies this distribution, and is available at
// http://www.apache.org/licenses/LICENSE-2.0

#include <Wire.h>
#include <Adafruit_BME280.h>
#include <SerialCom.h>
#include <Time.h>
#include "DS1307.h"
#include <MemoryFree.h>

#define ANEMO_PIN 3
#define WIND_VANE_PIN A1
#define DHTPIN 4     // what pin we're connected to

//Sampling durations  
#define P_SAMPLING_DURATION  30 //atmospheric pressure
#define T_SAMPLING_DURATION  30 //temperature
#define H_SAMPLING_DURATION  60 //humidity
#define WH_SAMPLING_DURATION 10 // wind heading
#define WS_SAMPLING_DURATION 2 //Wind speed

//Measurements and commands names 
#define ATMOSPHERIC_PRESSURE "A_PRESS"
#define TEMPERATURE "TEMP"
#define HUMIDITY "HUM"
#define WIND_HEADING "WIND_H"
#define WIND_SPEED "WIND_S"
#define GET_TIME "GT"
#define SET_TIME "ST"

// Anemometer parameters
#define ANEMO_RADIUS 0.09 //Anemometer radius in m
#define BOUNCE_DURATION 2
#define ALPHA_A 2.148 //Ponderation factor for anemo


// Wind vane  parameters
#define WIND_VANE_TOLERANCE 0.02




// Create object to handle connection to socket server
// Can use as well HardwareSerial as SoftwareSerial
SerialCom com(&Serial);
Adafruit_BME280 bme; // I2C
DS1307 clock; //define a objidentifier "Serial" is undefinedect of DS1307 class

//Previsous measurement times
time_t p_prev;
time_t t_prev;
time_t h_prev;
time_t wh_prev;
time_t ws_prev;

//Anemometer current values
float cur_wind_speed;
volatile unsigned long anemo_ticks;
volatile unsigned long contactBounceTime;

//Wind vane counters
float sinSum;
float cosSum;
float wh_count;

void setup() {

 
  attachInterrupt(
    digitalPinToInterrupt(ANEMO_PIN ),
    (void (*)())countAnemoTicks,
    FALLING
  );
  
  com.begin(9600);
  com.println("Arduino Started");


  clock.begin();
  
  if (!bme.begin()) {  
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    //while (1);
  }

  p_prev = now() + P_SAMPLING_DURATION;
  t_prev = now() + T_SAMPLING_DURATION;
  h_prev = now() + H_SAMPLING_DURATION;
  wh_prev = 0;
  ws_prev = 0;
  cur_wind_speed = 0;
  anemo_ticks = 0;
  contactBounceTime = 0;
  sinSum = 0;
  cosSum = 0;
  wh_count = 0;

  com.print("MEM ") ;com.println(freeMemory());
  
}

// This method receive command (cmd) from socket server and return resusts to it
void serialComHandler(char *cmd){
  if (strcmp(cmd,ATMOSPHERIC_PRESSURE) == 0) {
    getPress(1);
  }else if (strcmp(cmd,TEMPERATURE) == 0) {
    getTemp(1);
  }else if (strcmp(cmd,HUMIDITY) == 0) {
    getHumidity(1);
  }else if (strcmp(cmd,WIND_HEADING) == 0) {
    getWindHeading(1);
  }else if (strcmp(cmd,WIND_SPEED) == 0) {
    getWindSpeed(1);
  }else if (strcmp(cmd,GET_TIME) == 0) {
    getTime();
  }else if (strncmp(cmd,SET_TIME, strlen(SET_TIME)) == 0) {
    setTime(cmd+strlen(SET_TIME)+1);
  }
}

uint8_t near(int val, int ref){
  int low = ref*(1-WIND_VANE_TOLERANCE);
  int high = ref*(1+WIND_VANE_TOLERANCE);

  return (val >=low && val <= high);
}


//Return weathercock orientation as number for 0 (N) to 15 (N-NW) clockwise
// when weathercock power supply is 5V
int getOrientation(int v){
  int o;
  if (near(v, 787)){
    o=0;
  }else if (near(v, 407)){
    o=1;
  }else if(near(v, 462)){
    o=2;
  }else if (near(v, 82)){
    o=3;
  }else if (near(v, 92)){
    o=4;
  }else if (near(v, 64)){
    o=5;
  }else if (near(v, 185)){
    o=6;
  }else if (near(v, 126)){
    o=7;
  }else if (near(v, 288)){
    o=8;
  }else if (near(v, 245)){
    o=9;
  }else if (near(v, 633)){
    o=10;
  }else if (near(v, 602)){
    o=11;
  }else if (near(v, 946)){
    o=12;
  }else if (near(v, 829)){
    o=13;
  }else if (near(v, 889)){
    o=14;
  }else if (near(v, 705)){
    o=15;
  }else{
    o=16;
  }
  return o;
}
//Get and send atmospheric pressure:
// - if force 
// - if sampling duration is elapsed
void getPress(uint8_t force){
  if (now() - p_prev >= P_SAMPLING_DURATION  || force){
    com.print(ATMOSPHERIC_PRESSURE);com.print(" ");
    com.println(bme.readPressure()/100);
    if (!force){
      p_prev = now();
    }
  }
}

//Get and send temperature:
// - if force 
// - if sampling duration is elapsed
void getTemp(uint8_t force){
  if (now() - t_prev >= T_SAMPLING_DURATION  || force){
    //float temp = dht.readTemperature();
    float temp = bme.readTemperature();
    com.print(TEMPERATURE);com.print(" ");
    com.println(temp);
    if (!force){
      t_prev = now();
    }
  }
}
//Get and send humidity:
// - if force 
// - if sampling duration is elapsed
void getHumidity(uint8_t force){
  if (now() - h_prev >= H_SAMPLING_DURATION  || force){
    float hum = bme.readHumidity();
    com.print(HUMIDITY);com.print(" ");
    //com.println(bmp.readTemperature());
    com.println(hum);
    if (!force){
      h_prev = now();
    }
  }
}

//Get and send wind heading:
// - if force 
// - if sampling duration is elapsed

void getWindHeading(uint8_t force){
  float cur_heading;
  if (now() - wh_prev >= WH_SAMPLING_DURATION  || force){
    float avgSin;
    float avgCos;

    avgSin = sinSum/wh_count;
    avgCos = cosSum/wh_count;

    sinSum = 0;
    cosSum = 0;
    wh_count = 0;

    // Serial.print(avgSin, 4); Serial.print(" " ); Serial.println(avgCos, 4);
    cur_heading = atan2(avgSin, avgCos) / (2*PI)*360;
    // cur_heading = getOrientation(analogRead(WIND_VANE_PIN))*22.5;
    com.print(WIND_HEADING);com.print(" ");
    com.println(cur_heading);

    if (!force){
      wh_prev = now();
    }
  }else{
    cur_heading = getOrientation(analogRead(WIND_VANE_PIN))*2.0*PI;
    sinSum += sin(cur_heading);
    cosSum += cos(cur_heading);
    wh_count++;
  }
}

//Get and send last computed windspeed:
// - if force 
// - if sampling duration is elapsed, first computze windspeed
volatile void getWindSpeed(uint8_t force){
  if (now() - ws_prev >= WS_SAMPLING_DURATION  || force){
    if (!force){
      cli(); //Disable interrupts to avoid impacts on anemo_ticks
      float rps = ((float)anemo_ticks/2.0)/(float)(now() - ws_prev);
      cur_wind_speed = 2.0 * PI * ANEMO_RADIUS * rps * ALPHA_A;
      ws_prev = now();
      anemo_ticks = 0;
      contactBounceTime = millis(); 
      sei(); // Restart interrupt to count ticks
     
    }
    com.print(WIND_SPEED);com.print(" ");
    com.println(cur_wind_speed);
  }
}

//Register ticks from anemo (interrupts. theorical: 2/rotation):
volatile void countAnemoTicks(){
  if ((millis() - contactBounceTime) > BOUNCE_DURATION) { // debounce the switch contact. 
    anemo_ticks++; 
    contactBounceTime = millis(); 
  }   
}

//Return string as number ("len" first digits of str)
int getVal(char *str, uint8_t len){
  int rc;
  char bckup;

  bckup=str[len];
  str[len]=0;
  rc=atoi(str);
  str[len]=bckup;

  return rc;
  
}

//Set RTC time from iso string (YYYMMDDTHH:MI:SS)
//and send current RTC time
void setTime(char *isoDate){

  uint16_t year;
  uint8_t month, day, hour, min, sec;


  year=getVal(isoDate, 4);
  month=getVal(isoDate+5, 2);
  day=getVal(isoDate+8, 2);
  hour=getVal(isoDate+11, 2);
  min=getVal(isoDate+14, 2);
  sec=getVal(isoDate+17, 2);

  clock.fillByYMD(year,month,day);
  clock.fillByHMS(hour,min,sec);
  clock.setTime();

  getTime();
}


//Send current RTC time
void getTime(){
  clock.getTime();

  char iso_date[25];

  sprintf(
    iso_date,
    "%04d-%02d-%02dT%02d:%02d:%02d",
    clock.year+2000,
    clock.month,
    clock.dayOfMonth,
    clock.hour,
    clock.minute,
    clock.second
  );

  com.println(iso_date);
}

void loop() {
  com.handleSerialCom();
  getPress(0);
  getTemp(0);
  getHumidity(0);
  getWindHeading(0);
  getWindSpeed(0);
}
