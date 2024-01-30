#include <Arduino.h>
#include <ArduinoJson.h>


const int numberOfLEDs = 5;
const int LEDArrayPins[] = {2,3,4,5,6};

const int Sensorpin = A0;

//int value = 0;
void setup() {
  for (byte i = 0; i < numberOfLEDs; i++){ // set LED pins as output
    pinMode(LEDArrayPins[i], OUTPUT);
  }
  pinMode(Sensorpin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // read value
  
  int value =  analogRead(Sensorpin); // read sensor
  
  // scale value to between 0 and 1
  const  int maxValue = 1024;
  const int minValue = 0;
  float scaledValue = (value - minValue)/float(maxValue);

  // determine number of LEDs to light
  int numberToLight = scaledValue * (numberOfLEDs + 1);

  // light up corresponging number of LEDs
  for (byte i = 0; i < numberOfLEDs; i++){ //loop over LEDs
    if (i < numberToLight){
      digitalWrite(LEDArrayPins[i], HIGH);
    }
    else{
      digitalWrite(LEDArrayPins[i], LOW);
    }
  }
  String debugLine = "value: " + String(value) + " scaledValue: " + String(scaledValue) + " numberToLight: " + String(numberToLight);
  JsonDocument doc;
  doc["value"] = value ;
  doc["scaled value"] = scaledValue ;
  doc["number to light"] = numberToLight ; 

  Serial.println(debugLine);
  Serial.println(doc);

  delay(100);
  Serial.println("xxxx")
 }