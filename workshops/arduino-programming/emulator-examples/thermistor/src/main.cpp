#include <Arduino.h>
#include <SD.h>

#define CS_PIN 10

const float BETA = 3950; // should match the Beta Coefficient of the thermistor

File myFile;


void setup() {
  Serial.begin(9600);

  //Serial.print("Initializing SD card... ");

  //if (!SD.begin(CS_PIN)) {
  //  Serial.println("Card initialization failed!");
  //  while (true);
  //}

  //Serial.println("initialization done.");
}

void loop() {
  int analogValue = analogRead(A0);
  float celsius = 1 / (log(1 / (1023. / analogValue - 1)) / BETA + 1.0 / 298.15) - 273.15;
  Serial.print("Temperature: ");
  Serial.print(celsius);
  Serial.println(" ℃");
  delay(1000);
}
