#include <Arduino.h>

void setup() {
  // open a serial connection with baud rate (bits per second) of 9600
  Serial.begin(9600);

  Serial.println("I'm alive!");
}

float convertToCelcius(int analogueOutput){
   float celsius =  1 / (log(1 / (1023. / analogueOutput - 1)) / 3950 + 1.0 / 298.15) - 273.15;

   return celsius;
}


String JSONformatValues(float temperature, int analogueOutput){
  String JSONString = "{ \"temperature:\" " + String(temperature) + ", \"analogue value:\" "+ String(analogueOutput) +"}";

  return JSONString;
}


void printTemperature(){
  const int temperatureSensor = A0;
  int analogueValue = analogRead(temperatureSensor);
  float celsius = convertToCelcius(analogueValue);
  Serial.println(JSONformatValues(celsius, analogueValue));
  delay(2000);
}

void loop() {
  printTemperature();
}