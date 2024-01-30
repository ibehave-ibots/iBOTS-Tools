#include <Arduino.h>
#include <ArduinoJson.h>


const int Sensorpin = A0;

//int value = 0;
void setup() {
 
  pinMode(Sensorpin, INPUT);
  Serial.begin(115200);
}


struct DataPacket {
  int loopNum;
  int value;
};

int loopCounter = 0;
void loop() {

  loopCounter++;

  int sensorValue =  analogRead(Sensorpin); // read sensor
  //int value[] = {loopCounter, sensorValue };
  int value[] = {loopCounter,int(sensorValue) };
 
 
  Serial.write( (byte*)&value , sizeof(value));

  delay(20);
 }