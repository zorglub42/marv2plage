// Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Apache License, Version 2.0
// which accompanies this distribution, and is available at
// http://www.apache.org/licenses/LICENSE-2.0

#define getOrientation getOrientation5V
#define TOLERANCE 0.02

char *roseDesVents[]={"N", "N-NE","NE","E-NE","E", "E-SE", "SE", "S-SE", "S", "S-SW", "SW", "W-SW", "W", "W-NW", "NW", "N-NW", "N/D"};


uint8_t near(int val, int ref){
  int low = ref*(1-TOLERANCE);
  int high = ref*(1+TOLERANCE);

  return (val >=low && val <= high);
}

int getOrientation5V(int v){
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

int getOrientation3_3V(int v){
  int o;
  if (610 <= v & v <= 650){
    o=0;
  }else if (540 <= v && v <= 570){
    o=1;
  }else if(580 <= v && v <= 609){
    o=2;
  }else if (450 <= v && v <= 500){
    o=3;
  }else if (501 <= v && v <= 550){
    o=4;
  }else if (250 <= v && v <= 300){
    o=5;
  }else if (300 <= v && v<= 350){
    o=6;
  }else if (50 <= v && v<= 57){
    o=7;
  }else if (58 <= v && v<= 70){
    o=8;
  }else if (35 <= v && v<= 50){
    o=9;
  }else if (110 <= v && v<= 150){
    o=10;
  }else if (75 <= v && v<= 90){
    o=11;
  }else if (170 <= v && v<= 200){
    o=12;
  }else if (150 <= v && v<= 170){
    o=13;
  }else if (410 <= v && v<= 450){
    o=14;
  }else if (350 <= v && v<= 410){
    o=15;
  }else{
    o=16;
  }
  return o;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int v = analogRead(A1);
  int orientation = getOrientation(v);
  float heading = float(orientation * 22.5);
  Serial.print(v); Serial.print(" ");Serial.print(roseDesVents[orientation]);Serial.print(" "); Serial.println(heading);
//Serial.println(v);
  delay(300);
}
