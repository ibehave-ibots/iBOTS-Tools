#include <Arduino.h>



int delayValue_ms = 500;
int loopCounter = 0;
bool signalDetected = false;

const int LEDpin = 3;
const int Sensorpin = A0;

const int TriggerValue = 500; // set trigger value

void setup() {
  pinMode(LEDpin, OUTPUT);
  pinMode(Sensorpin, INPUT);
  Serial.begin(9600);
}

void loop() {
  
  int analogValue = analogRead(Sensorpin); // read sensor

  
  String data = String(loopCounter) + " " + String(analogValue);
  Serial.println(data);
  digitalWrite(LEDpin, HIGH);
  delay(delayValue_ms);
  digitalWrite(LEDpin, LOW);
  loopCounter ++;
}