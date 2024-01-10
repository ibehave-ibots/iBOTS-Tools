#include <Arduino.h>

const int LEDpin = 3;
//const int LEDpin = LED_BUILTIN; // use built in LED on Arduino
const int Sensorpin = A0;


const int TriggerValue = 500; // set trigger value

void setup() {
  pinMode(LEDpin, OUTPUT);
  pinMode(Sensorpin, INPUT);
  Serial.begin(9600);
}

void loop() {
  
  int analogValue = analogRead(Sensorpin); // read sensor

  if (analogValue > TriggerValue){digitalWrite(LEDpin, HIGH);} // turn LED on
  else{digitalWrite(LEDpin, LOW);} // turn LED off

  Serial.println(analogValue);
  delay(100);
}
