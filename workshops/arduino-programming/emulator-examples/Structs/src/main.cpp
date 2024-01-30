#include <Arduino.h>


const int lightSensorPin = 12; 
const int motionSensorPin = 13;

const float delayTime_s = 1.0;

int loopCounter = 0;

struct dataFromSensor{
   float time;
   int motionSensor;
   int lightSensor;
};

void printDataFromSensor(dataFromSensor d){
  Serial.println(d.time );
  Serial.println(d.motionSensor);
}
void setup() {
  pinMode(lightSensorPin, INPUT_PULLUP);
  pinMode(motionSensorPin, INPUT_PULLUP);

  Serial.begin(9600);
}

void loop() {
  int motionSensorValue = digitalRead(motionSensorPin);
  int lightSensorValue = digitalRead(lightSensorPin);

  //Serial.println(String(motionSensorValue)+ " "+ String(lightSensorValue));

  dataFromSensor data = dataFromSensor{delayTime_s*loopCounter,motionSensorValue,lightSensorValue };
  printDataFromSensor(data);
  delay(delayTime_s*1000);
  loopCounter++;
}

