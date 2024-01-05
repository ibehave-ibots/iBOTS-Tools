#include <Arduino.h>

#include "greenbtn.h"
#include "yellowbtn.h"
#include "redbtn.h"
#include "ldrresponse.h"

#define GreenButton 11
#define YellowButton 10
#define RedButton 9

#define RedLED 3
#define RedLED 4
#define RedLED 5

#define SPEAKER_PIN 8
#define LDR_PIN 12

void setup() {
  pinMode(RedLED, OUTPUT); 
  pinMode(RedLED, OUTPUT); 
  pinMode(RedLED, OUTPUT); 
  pinMode(SPEAKER_PIN, OUTPUT);

  pinMode(GreenButton, INPUT_PULLUP);
  pinMode(YellowButton, INPUT_PULLUP);
  pinMode(RedButton, INPUT_PULLUP);

  Serial.begin(115200);

}


void loop() {
  if (digitalRead(GreenButton)==LOW){
    GreenButtonAction();
  }

  if (digitalRead(YellowButton)==LOW){
    YellowButtonAction();
  }

  if (digitalRead(RedButton)==LOW){
    RedButtonAction();
  }

  LdrResponse();

  
}
