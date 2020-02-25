// Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Apache License, Version 2.0
// which accompanies this distribution, and is available at
// http://www.apache.org/licenses/LICENSE-2.0

#include <Time.h>


#define ANEMO_PIN 3
#define SAMPLING_DURATION 5
#define BOUNCE_DURATION 1

volatile unsigned long ticks;
volatile unsigned long contactBounceTime;
int prev;

void setup() {
  pinMode(ANEMO_PIN, INPUT);

  attachInterrupt(digitalPinToInterrupt(ANEMO_PIN ), (void (*)())countTicks, FALLING);
  ticks = 0;
  Serial.begin(9600);

  Serial.println("Starting");
  contactBounceTime=0;
  prev = now();
}

volatile void printAnemoSpeed(){
  if (now() - prev>= SAMPLING_DURATION){
    Serial.println(ticks);
    /*float rps = ((float)ticks/2.0)/(float)SAMPLING_DURATION;
    float spd = rps * 2 * PI * 0.072;
    Serial.print("RPS="); Serial.print(rps, 4);;
    Serial.print(" SPEED="); Serial.print(spd, 4); Serial.println(" m/s");*/
    cli();
    prev = now();
    ticks = 0;
    sei();
  }
  
}
// Boucle principale:
void loop() {
  printAnemoSpeed();
}



volatile void countTicks(){
  /*//ticks++;
  if (digitalRead(ANEMO_PIN)){
    ticks++;

    //Ensure state have changed from LOW to HIGH before releasing CPU for next operation (interrupt, main loop.....) 
    do {
      delayMicroseconds(5000);
    }while (digitalRead(ANEMO_PIN));
  }*/

  
  if ((millis() - contactBounceTime) > BOUNCE_DURATION) { // debounce the switch contact. 
    ticks++; 
    contactBounceTime = millis(); 
  }   
  
}

