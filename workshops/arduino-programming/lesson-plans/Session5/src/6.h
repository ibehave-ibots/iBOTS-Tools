#include <Arduino.h>


void display_6(){
    //set all pins to high to clear display
  int segmentPins[] = {6,7,8,9,10,11,12};
  for (int i =0; i < 7; i++){ 
    digitalWrite(segmentPins[i], HIGH);
  }

  int segmentsToLight[] = {6,8,9,10,11,12};
   for (int i = 0; i < 6; i++){ 
    digitalWrite(segmentsToLight[i], LOW);
  }
}