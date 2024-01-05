#include <Arduino.h>
#include "pitches.h"

#define RedLED 3
#define RedLED 4
#define RedLED 5

#define SPEAKER_PIN 8

void YellowButtonAction(){
  tone(SPEAKER_PIN, NOTE_C4,500);
}