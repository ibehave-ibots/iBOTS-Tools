#include <Arduino.h>
#include <ArduinoJson.h>



const int AnalogueSensorPin = A0; 
const int DigitalSensorPin = 13;
const int LEDpin = 2;
const float delayTime_ms = 50;


void setup() {
  pinMode(AnalogueSensorPin, INPUT);
 pinMode(DigitalSensorPin, INPUT_PULLUP);

 pinMode(LEDpin, OUTPUT);
  Serial.begin(9600);
}

const int printEvery = 4;
int dataCounter =1;

const int capacity = JSON_ARRAY_SIZE(3) + printEvery*JSON_OBJECT_SIZE(3);
StaticJsonDocument<10024> jsonData; // number in brackets in bytes! When the object is full, no more data can be added!

void loop() {
  
  int analogueSensorValue = analogRead(AnalogueSensorPin);
  int digitalSensorValue = digitalRead(DigitalSensorPin);

  if (digitalSensorValue == HIGH){
    digitalWrite(LEDpin, HIGH);
  }
  else{
        digitalWrite(LEDpin,LOW);

  }


  jsonData[(dataCounter-1) % printEvery]["loop number"] = dataCounter;
  jsonData[(dataCounter -1) % printEvery]["analogue sensor value"] = analogueSensorValue;
  jsonData[(dataCounter -1) % printEvery]["digital sensor value"] = digitalSensorValue;

  
  if (dataCounter % printEvery == 0 & dataCounter>1){
   
     serializeJson(jsonData, Serial);
    Serial.println(); // force new line
    StaticJsonDocument<capacity> jsonData;

  }
  
  delay(delayTime_ms);
  dataCounter++;
}

