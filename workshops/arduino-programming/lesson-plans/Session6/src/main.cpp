#include <Arduino.h>
#include <SD.h>
#include <ArduinoJson.h>
#include <Blinkenlight.h>


const int CS_PIN = 10;
const int LEDPin = LED_BUILTIN;
const int switchPin = 2;


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

  pinMode(switchPin, INPUT);

  Serial.begin(115200);

  Serial.print("Initializing SD card... ");

  if (!SD.begin(CS_PIN)) {
    Serial.println("Card initialization failed!");
    while (true);
  }
  

  read_file(dataFileName);

  Serial.println("initialization done.");
  // initialise output file with header
  write_line_to_file(dataFileName, "time, analogue_value, temperature");

}


float timeValue = 0; 
float sampleInterval_s = 2;


Blinkenlight myLed(LEDPin);

void loop() {

  myLed.blink();

  int analogValue = analogRead(A0);
  float celsius = 1 / (log(1 / (1023. / analogValue - 1)) / 3950.0 + 1.0 / 298.15) - 273.15;
  String dataToWrite = String (timeValue) + ", "+ String(analogValue) + ", " + String(celsius) ;

    
  JsonDocument doc;
  doc["temperature"] = celsius; 
  doc["analogue value"] = analogValue;
  doc["time"] = timeValue;

  serializeJson(doc, Serial);
  Serial.println(); // force new line



  //digitalWrite(LEDPin, HIGH);
  write_line_to_file(dataFileName, dataToWrite);
  //digitalWrite(LEDPin, LOW);


  delay(1000*sampleInterval_s);
  timeValue = timeValue + sampleInterval_s;

  if (digitalRead(switchPin)== LOW){
    read_file(dataFileName);
    exit(0);
  }
    
}
