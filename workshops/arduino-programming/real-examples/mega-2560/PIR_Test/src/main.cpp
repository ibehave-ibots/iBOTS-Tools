#include <Arduino.h>

// put function declarations here:
int myFunction(int, int);


const int sensorPin = 53;
void setup() {
pinMode(sensorPin, INPUT);
Serial.begin(9600);
}

void loop() {
  int signal = digitalRead(sensorPin);
  //int signal = analogRead(sensorPin);
  if (signal == HIGH){
    Serial.println("movement");
  }
  Serial.println(signal);
  delay(500);
}

