#include <Arduino.h>

const int redLED = 3;
int greenLED = 4;
int purpleLED = 5;
int delay_time_s = 1;
int delay_time_ms = delay_time_s*1000;
void setup() {
  pinMode(redLED, OUTPUT); 
  pinMode(greenLED, OUTPUT);
  pinMode(purpleLED, OUTPUT);
}

void loop() {
  digitalWrite(redLED, HIGH); 
  delay(delay_time_ms); 
  digitalWrite(redLED, LOW); 
  delay(delay_time_ms); 
  redLED++;
}