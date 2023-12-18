#include <Arduino.h>
#include <SD.h>

#define CS_PIN 10

String dataFileName = "tdata.txt";

void write_line_to_file(String fileName, String line){
    File file_to_write;
    file_to_write = SD.open(fileName, FILE_WRITE);

    if (file_to_write){
      file_to_write .println(line);
      file_to_write.close();
    } else{
          Serial.println("error opening file");
    }
}

void read_file(String fileName){
  File file;
  file = SD.open(fileName);
  if (file) {
    while (file.available()) { // read from the file until there's nothing else in it:
      Serial.write(file.read());
    }
    // close the file:
    file.close();
  } else { // if the file didn't open, print an error:
    Serial.println("error opening file");
  }
}

void setup() {
  Serial.begin(115200);

  Serial.print("Initializing SD card... ");

  if (!SD.begin(CS_PIN)) {
    Serial.println("Card initialization failed!");
    while (true);
  }

  Serial.println("initialization done.");
  // initialise output file with header
  write_line_to_file(dataFileName, "time, analogue_value, temperature");

}


float timeValue = 0; 
float sampleInterval_s = 2;
const float BETA = 3950; // should match the Beta Coefficient of the thermistor
void loop() {
  int analogValue = analogRead(A0);
  float celsius = 1 / (log(1 / (1023. / analogValue - 1)) / BETA + 1.0 / 298.15) - 273.15;
  timeValue += sampleInterval_s;
  String dataToWrite = String (timeValue) + ", "+ String(analogValue) + ", " + String(celsius) ;
  write_line_to_file(dataFileName, dataToWrite);

  //read_file("test.txt");
  
  // re-open the file for reading:
  read_file(dataFileName);

  delay(1000*sampleInterval_s);

    
}




