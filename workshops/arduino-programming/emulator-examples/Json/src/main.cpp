#include <Arduino.h>
#include <ArduinoJson.h>



const int lightSensorPin = 12; 
const int motionSensorPin = 13;

const float delayTime_s = 1.0;


void setup() {
  pinMode(lightSensorPin, INPUT_PULLUP);
  pinMode(motionSensorPin, INPUT_PULLUP);

  Serial.begin(9600);
}

const int printEvery = 5;
int dataCounter =1;

const int capacity = JSON_ARRAY_SIZE(3) + printEvery*JSON_OBJECT_SIZE(3);
StaticJsonDocument<1024> jsonData; // number in brackets in bytes! When the object is full, no more data can be added!

void loop() {
  
  int motionSensorValue = digitalRead(motionSensorPin);
  int lightSensorValue = digitalRead(lightSensorPin);

  jsonData[(dataCounter-1) % printEvery]["loop number"] = dataCounter;
  jsonData[(dataCounter -1) % printEvery]["motion sensor value"] = motionSensorValue;
  jsonData[(dataCounter -1) % printEvery]["light sensor value"] = lightSensorValue;
  
  if (dataCounter % printEvery == 0 & dataCounter>1){
    Serial.println("XXXXXXXXXXXXXXXXXXXXXX");
     serializeJsonPretty(jsonData, Serial);
    Serial.println(); // force new line
    StaticJsonDocument<capacity> jsonData;

  }
  
  delay(delayTime_s*1000);
  dataCounter++;
}

