#include <Arduino.h>

const int numberOfLEDs = 2;
const int LEDArrayPins[] = {3, LED_BUILTIN};

const int Sensorpin = 13;

void setup() {
  for (byte i = 0; i < numberOfLEDs; i++){ // set LED pins as output
    pinMode(LEDArrayPins[i], OUTPUT);
  }

  Serial.begin(9600);
}

void loop() {
  // read digital value
  const  int maxValue = 200;
  const int minValue = 50;
  int digitalValue =  19;//random(minValue, maxValue); // simulate sensor with random number 
  
  // scale digital value to between 0 and 1
  float scaledValue = (digitalValue - minValue)/float(maxValue);

  // determine number of LEDs to light
  int numberToLight = scaledValue * numberOfLEDs + 1;

  // light up corresponging number of LEDs
  for (byte i = 0; i < numberOfLEDs; i++){ //loop over LEDs
    if (i < numberToLight){
      digitalWrite(LEDArrayPins[i], HIGH);
    }
    else{
      digitalWrite(LEDArrayPins[i], LOW);
    }
  }
  String debugLine = "digitalValue: " + String(digitalValue) + " scaledValue: " + String(scaledValue) + " numberToLight: " + String(numberToLight);
  Serial.println(debugLine);

  delay(5000);
 }

