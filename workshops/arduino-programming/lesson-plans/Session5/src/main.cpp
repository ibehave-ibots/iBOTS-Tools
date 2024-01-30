#include <Arduino.h>
#include <4.h>
#include <6.h>

void setup() {
  int allPins[] = {2,3,6,7,8,9,10,11,12}; // define pins to set as outputs
  for (int i = 0; i < 9; i++){ 
    pinMode(allPins[i], OUTPUT);
  }

  digitalWrite(2,HIGH); // set pin 2 as HIGH to turn on 1st digit

}



void display_5(){
    //set all pins to high to clear display
  int segmentPins[] = {6,7,8,9,10,11,12};
  for (int i =0; i < 7; i++){ 
    digitalWrite(segmentPins[i], HIGH);
  }

  int segmentsToLight[] = {6,8,9,11,12};
   for (int i = 0; i < 5; i++){ 
    digitalWrite(segmentsToLight[i], LOW);
  }
}

void loop() {
  display_4();
  delay(1000);
  display_5();
  delay(1000);
  display_6();
  delay(1000);
}