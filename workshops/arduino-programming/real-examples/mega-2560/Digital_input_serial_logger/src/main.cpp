#include <Arduino.h>


const int LEDpin = 2;

const int DigitalInputPin = 13;


void setup() {
  pinMode(LEDpin, OUTPUT);
  pinMode(DigitalInputPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  
  int DigitalValue = digitalRead(DigitalInputPin); // read value of digital device
  if(DigitalValue == HIGH){
    Serial.println("INPUT HIGH");
    digitalWrite(LEDpin, HIGH);
  }
  else{
    digitalWrite(LEDpin, LOW);
  }
  delay(100);
}

