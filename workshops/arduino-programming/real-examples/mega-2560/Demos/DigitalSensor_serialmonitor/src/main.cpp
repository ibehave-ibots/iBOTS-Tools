#include <Arduino.h>

const int numberOfLEDs = 3;
const int LEDArrayPins[] = {45,43,41};
const int sensorPin = 25;

void setup() {
  for (byte i = 0; i < numberOfLEDs; i++){ // set LED pins as output
    pinMode(LEDArrayPins[i], OUTPUT);
  }

  pinMode(sensorPin, INPUT_PULLUP);
pinMode(A0, INPUT);
  Serial.begin(9600);
}

int numberToLight = 0;
int loopCounter=0;
void loop() {

  Serial.println(analogRead(A0));
  loopCounter++;
  // read sensor
  int sensorValue = digitalRead(sensorPin);
  if (sensorValue == LOW){
     Serial.println(String(loopCounter)+ " DETECTION!");
     numberToLight++;
     numberToLight = numberToLight %  (numberOfLEDs+1); // wrap around LEDs
  }

  // light LEDs 
  for (byte i = 0; i < numberOfLEDs; i++){ 
    if (i < numberToLight){
      digitalWrite(LEDArrayPins[i], HIGH);
    }
    else{
      digitalWrite(LEDArrayPins[i], LOW);
    }
  }

  delay(20);
 
}
