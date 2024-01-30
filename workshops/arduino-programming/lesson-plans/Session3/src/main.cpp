#include <Arduino.h>

// variables for components on each pin
const int GreenButton = 11;
const int YellowButton = 10;
const int RedButton = 9;

const int RedLED = 3;
const int GreenLED = 4;
const int PurpleLED = 5;

const int Speaker = 8;
const int LightSensor = 12;


void setup() {
  pinMode(RedLED, OUTPUT); 
  pinMode(GreenLED, OUTPUT); 
  pinMode(PurpleLED, OUTPUT); 
  pinMode(Speaker, OUTPUT);

  pinMode(GreenButton, INPUT_PULLUP);
  pinMode(YellowButton, INPUT_PULLUP);
  pinMode(RedButton, INPUT_PULLUP);

  pinMode(LightSensor, INPUT);

}


void shortFlash(int LEDToFlash){
  
  digitalWrite(LEDToFlash, HIGH); 
  delay(200);
  digitalWrite(LEDToFlash, LOW);
  delay(200);
}

void longFlash(int LEDToFlash){

  digitalWrite(LEDToFlash, HIGH); 
  delay(500);
  digitalWrite(LEDToFlash, LOW);
  delay(500);
}

void SOS(int LEDToFlash){

  // 3 short flashes
  shortFlash(LEDToFlash); 
  shortFlash(LEDToFlash); 
  shortFlash(LEDToFlash); 
  delay(1000);

  // 3 long flashes
  longFlash(LEDToFlash);
  longFlash(LEDToFlash);
  longFlash(LEDToFlash);
  delay(1000);

  // 3 short flashes
  shortFlash(LEDToFlash); 
  shortFlash(LEDToFlash); 
  shortFlash(LEDToFlash); 
}

void lightSensorResponse(){
if (digitalRead(LightSensor)== HIGH){
 digitalWrite(PurpleLED,HIGH);
}
else{
  digitalWrite(PurpleLED,LOW);
}

}

void loop() {
   
  if (digitalRead(RedButton)==LOW){
       SOS(RedLED);
       delay(100);
       SOS(GreenLED);
  }

  if (digitalRead(GreenButton)==LOW){
       longFlash(GreenLED);
  }

  lightSensorResponse();
     
}