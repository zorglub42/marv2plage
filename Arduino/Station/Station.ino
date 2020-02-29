// Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Apache License, Version 2.0
// which accompanies this distribution, and is available at
// http://www.apache.org/licenses/LICENSE-2.0


// Compilation directives (optional features)
//#define WITH_COMPASS  //Uncomment if version support magnetic compass
#define WITH_PWR_CTL  //Uncomment if version support battery load measurement
#define WITH_SCREEN   //Uncomment if version support LCD screen


// Include
#include <Wire.h>
#include <SerialCom.h>
#include <Time.h>
#include <MemoryFree.h>
#include <Adafruit_BME280.h>


//Common defines and globals
#define RAD2DEG 57.295800025114424159

#define ANEMO_PIN 3
#define WIND_VANE_PIN A1
#define DHTPIN 4     // what pin we're connected to

#ifdef WITH_SCREEN
  #include <SoftwareSerial.h>

  #define LCD_TX 4
  #define LCD_RX 5
  #define LCD_BAUD 9600
  #define BUTTON_PIN 6
  #define DISPLAY_METRICS "DM"

  #define NO_CLICK 0
  #define SHORT_CLICK 1
  #define LONG_CLICK 2

  #define DISPLY_DURATION 2000

  #define lcdPrint(v) lcd.print(v);
  #define lcdPrint1(line1) clearDisplay();setLCDCursor(0);lcd.print(line1);
  #define lcdPrint2(line1, line2) clearDisplay();setLCDCursor(0);lcd.print(line1);setLCDCursor(16);lcd.print(line2);
  #define lcdPrintL1(line) setLCDCursor(0);lcd.print(line);
  #define lcdPrintL2(line) setLCDCursor(16);lcd.print(line);

  String roseDesVents[]={"N", "N-NE","NE","E-NE","E", "E-SE", "SE", "S-SE", "S", "S-SW", "SW", "W-SW", "W", "W-NW", "NW", "N-NW", "N/D"};
  SoftwareSerial lcd(LCD_TX, LCD_RX);

#endif

#ifdef WITH_PWR_CTL
  // Battery load control
  #define PWR_1 8
  #define PWR_2 9
  #define PWR_3 10
  #define PWR_4 11
  #define PWR_SWITCH 7

  #define PWR_SAMPLING_DURATION 60
  #define POWER_LOAD "PWR_LOAD"

  time_t pwr_prev;
#endif


#ifdef WITH_COMPASS
  #include <MPU9250.h>
  #include <EEPROM.h>
  #define MAG_SAMPLING_DURATION 5 //Mag heading
  #define CAL_MAG "CM"
  #define MAG_SHIFT "MS"
  #define HAVE_COMPASS "HC"
  #define CALIBRATION_COUNT 500
  #define CAL_HEADER 42

  typedef struct {
    float biasX;
    float biasY;
    float biasZ;
    float scaleX;
    float scaleY;
    float scaleZ;
  } mag_params;

  unsigned int magShift;
#endif
//Sampling durations  
#define P_SAMPLING_DURATION  30 //atmospheric pressure
#define T_SAMPLING_DURATION  30 //temperature
#define H_SAMPLING_DURATION  30 //humidity
#define WH_SAMPLING_DURATION 10 // wind heading
#define WS_SAMPLING_DURATION 2 //Wind speed

//Measurements and commands names 
#define ATMOSPHERIC_PRESSURE "A_PRESS"
#define TEMPERATURE "TEMP"
#define HUMIDITY "HUM"
#define WIND_HEADING "WIND_H"
#define WIND_SPEED "WIND_S"

// Anemometer parameters
#define ANEMO_RADIUS 0.09 //Anemometer radius in m
#define BOUNCE_DURATION 2
//#define ALPHA_A 2.148 //Ponderation factor for anemo (JM etalonage)
#define ALPHA_A 2.5


// Wind vane  parameters
#define WIND_VANE_TOLERANCE 0.02





// Create object to handle connection to socket server
// Can use as well HardwareSerial as SoftwareSerial
SerialCom com(&Serial);
Adafruit_BME280 bme; // I2C

#ifdef WITH_COMPASS
  MPU9250 mpu(Wire,0x68);
#endif

//Previsous measurement times
time_t p_prev;
time_t t_prev;
time_t h_prev;
time_t wh_prev;
time_t ws_prev;

//Anemometer current values
volatile unsigned long anemo_ticks;
volatile unsigned long contactBounceTime;

//Wind vane counters
float sinSum;
float cosSum;
float wh_count;

float cur_wind_speed;

#ifdef WITH_SCREEN
  void setBacklight(byte brightness)
  {
    lcd.write(0x80);  // send the backlight command
    lcd.write(brightness);  // send the brightness value
  }

  void clearDisplay()
  {
    lcd.write(0xFE);  // send the special command
    lcd.write(0x01);  // send the clear screen command
  }

  void setLCDCursor(byte cursor_position)
  {
    lcd.write(0xFE);  // send the special command
    lcd.write(0x80);  // send the set cursor command
    lcd.write(cursor_position);  // send the cursor position
  }

  void displayMetrics(){
      setBacklight(255);
      clearDisplay();
      lcdPrint1(F("Vitesse : "));
      lcd.print(cur_wind_speed * 1.94384, 2 );
      lcdPrintL2(F("Dir. : "));
      lcd.print(roseDesVents[getOrientation(analogRead(WIND_VANE_PIN))]);
      delay(DISPLY_DURATION);
      shutdownDisplay();

  }
  void shutdownDisplay(){
      setBacklight(0);
      clearDisplay();
  }

  uint8_t getButton(){
    unsigned long start = millis();
    while (digitalRead(BUTTON_PIN) && (millis() - start) < 1010){
      delay(10);
    }
    unsigned long stop = millis();
    if ((stop - start) < 10) return NO_CLICK;
    if ((stop - start) < 1000) return SHORT_CLICK;
    return LONG_CLICK;

  }

  #ifdef WITH_PWR_CTL
  void displayPower(){
    setBacklight(255);
    clearDisplay();
    lcdPrint1(F("Batt. : "));
    lcd.print(getBatteryLoad(1));
    lcd.print(" %");
    delay(DISPLY_DURATION);
    shutdownDisplay();
  }
  #endif
  void checkDisplay(){
    uint8_t butt = getButton();

    #ifndef WITH_PWR_CTL
    if (butt){
    #else
    if (butt == LONG_CLICK){
      displayPower();
    }else if (butt == SHORT_CLICK){
    #endif
      displayMetrics();
    }
  }
#endif

#ifdef WITH_PWR_CTL
  int getBatteryLoad(int8_t force){

    if (now() - pwr_prev >= PWR_SAMPLING_DURATION  || force){
      digitalWrite(PWR_SWITCH, HIGH);
      delay(100);
    
      int8_t load = 0;
      if (digitalRead(PWR_1)) load+=25;
      if (digitalRead(PWR_2)) load+=25;
      if (digitalRead(PWR_3)) load+=25;
      if (digitalRead(PWR_4)) load+=25;
      digitalWrite(PWR_SWITCH, LOW);
      
      com.print(POWER_LOAD);com.print(" ");
      com.println(load);
      if (!force) pwr_prev = now();
      return load;
    }
    return -1;
  }
#endif

#ifdef WITH_COMPASS
  unsigned int getMagShift(){
    unsigned long start = now();
    float count = 0;
    float sins, coss;
    unsigned int heading;

    sins = coss = 0;
    while (now() - start < MAG_SAMPLING_DURATION){
      heading = getMagHeading();
      sins += sin(heading*0.017453298768179);
      coss += cos(heading*0.017453298768179);
      count++;
    }
    heading=atan2(sins/count, coss/count)*RAD2DEG;
    return (heading+360)%360;
  }
#endif

void setup() {

 
  attachInterrupt(
    digitalPinToInterrupt(ANEMO_PIN ),
    (void (*)())countAnemoTicks,
    FALLING
  );
  

  com.begin(9600);
  com.println(F("Arduino Starting"));

  if (!bme.begin()) {  
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    //while (1);
  }else{
    Serial.println(F("BME280 Started"));
  }

  #ifdef WITH_COMPASS
    if (!mpu.begin()<0){
      Serial.println(F("MPU9250 Initialization failed"));
    }else{
      Serial.println(F("MPU9250 Started"));
    }

    if (!getMagCalibration()){
      Serial.println(F("MPU9250 not calibrated. Calibrating...."));
      calibrateMag();
    }
    mpu.calibrateMag(200);
  #else
    Serial.println(F("Not using mag compass"));
  #endif
  
  #ifdef WITH_SCREEN
      pinMode(BUTTON_PIN, INPUT);
      lcd.begin(LCD_BAUD);  // Start the LCD at 9600 baud
      shutdownDisplay();
  #endif

  wh_prev = 0;
  ws_prev = 0;
  cur_wind_speed = 0;
  anemo_ticks = 0;
  contactBounceTime = 0;
  sinSum = 0;
  cosSum = 0;
  wh_count = 0;
  p_prev = now() + P_SAMPLING_DURATION;
  t_prev = now() + T_SAMPLING_DURATION;
  h_prev = now() + H_SAMPLING_DURATION;
  wh_prev = now();

  #ifdef WITH_COMPASS
    magShift = getMagShift();
  #endif
  #ifdef WITH_PWR_CTL
    pinMode(PWR_SWITCH, OUTPUT);
    pinMode(PWR_1, INPUT);
    pinMode(PWR_2, INPUT);
    pinMode(PWR_3, INPUT);
    pinMode(PWR_4, INPUT);
    pwr_prev = now() + PWR_SAMPLING_DURATION;
  #endif

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
  #ifdef WITH_COMPASS
  }else if (strcmp(cmd,CAL_MAG) == 0) {
    calibrateMag();
    com.println(F("CALIBRATION READY"));
  }else if (strcmp(cmd, MAG_SHIFT) == 0) {
    magShift = getMagShift();
    com.print("MAG SHIFT ");
    com.println(magShift);
  }else if (strcmp(cmd, HAVE_COMPASS) == 0){
    com.print(HAVE_COMPASS); com.println(" 1");
  #endif
  #ifdef WITH_PWR_CTL
  }else if (strcmp(cmd, POWER_LOAD) == 0){
    getBatteryLoad(1);
  #endif
  #ifdef WITH_SCREEN
  }else if (strcmp(cmd, DISPLAY_METRICS) == 0){
    displayMetrics();
    delay(2000);
    shutdownDisplay();
    com.print("DONE");
  #endif
  }
}

#ifdef WITH_COMPASS
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

  unsigned getMagHeading(){
      mpu.readSensor();
      // display the data
      float x = mpu.getMagX_uT();
      float y = mpu.getMagY_uT();
      long heading = atan2(y, x)*RAD2DEG;
      heading = (heading+360)%360;
      return heading;
  }
#endif


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

    // Serial.print(avgSin, 4); Serial.print(" " ); Serial.print(avgCos, 4);
    cur_heading = atan2(avgSin, avgCos) *RAD2DEG;
    #ifdef WITH_COMPASS
    cur_heading = int(cur_heading + magShift + 360)%360;
    #endif
    
    // cur_heading = getOrientation(analogRead(WIND_VANE_PIN))*22.5;
    com.print(WIND_HEADING);com.print(" ");
    com.println(cur_heading);

    if (!force){
      wh_prev = now();
    }
  }else{
    cur_heading = getOrientation(analogRead(WIND_VANE_PIN)) * 22.5; // Get orientation in deg
    cur_heading = cur_heading * 0.0174533; //convert deg to rad
    // Serial.println(cur_heading);
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

void loop() {
  com.handleSerialCom();
  getPress(0);
  getTemp(0);
  getHumidity(0);
  getWindHeading(0);
  getWindSpeed(0);
#ifdef WITH_PWR_CTL
  getBatteryLoad(0);
#endif
#ifdef WITH_SCREEN
  checkDisplay();
#endif
}
