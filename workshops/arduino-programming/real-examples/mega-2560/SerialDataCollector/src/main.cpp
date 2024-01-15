#include <Arduino.h>

int counter=1;
void setup() {
     Serial.begin(9600);
}


void loop(){
     Serial.println(String(counter)+ " : Hello tout le monde");
     delay(1000*10);
     counter++;
}