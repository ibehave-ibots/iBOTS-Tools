#include <Arduino.h>
#include <SD.h>

#define CS_PIN 10

File root;
File myFile;


void printDirectory(File dir, int numTabs) {
  while (true) {

    File entry =  dir.openNextFile();
    if (! entry) {
      // no more files
      break;
    }
    for (uint8_t i = 0; i < numTabs; i++) {
      Serial.print('\t');
    }
    Serial.print(entry.name());
    if (entry.isDirectory()) {
      Serial.println("/");
      printDirectory(entry, numTabs + 1);
    } else {
      // files have sizes, directories do not
      Serial.print("\t\t");
      Serial.println(entry.size(), DEC);
    }
    entry.close();
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

  Serial.println("Files in the card:");
  root = SD.open("/");
  printDirectory(root, 0);
  Serial.println("");

  // Example of reading file from the card:
  //File textFile = SD.open("wokwi.txt");
  //if (textFile) {
  //  Serial.print("wokwi.txt: ");
  //  while (textFile.available()) {
  //    Serial.write(textFile.read());
  //  }
  //  textFile.close();
  //} else {
  //  Serial.println("error opening wokwi.txt!");
  //}
}

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

void loop() {
  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  //myFile = SD.open("test.txt", FILE_WRITE);

  // if the file opened okay, write to it:
  // if (myFile) {
  //   Serial.print("Writing to test.txt...");
  //   myFile.println("testing 1, 2, 3.");
  //   // close the file:
  //   myFile.close();
  //   Serial.println("done.");
  // } else {
  //   // if the file didn't open, print an error:
  //   Serial.println("error opening test.txt");
  // }
  write_line_to_file("test.txt", "this is a not line");

  //read_file("test.txt");
  Serial.println("aaaaaaaa");
  // re-open the file for reading:
  myFile = SD.open("test.txt");
  // if (myFile) {
  //   Serial.println("test.txt:");

  //   // read from the file until there's nothing else in it:
  //   while (myFile.available()) {
  //     Serial.write(myFile.read());
  //   }
  //   // close the file:
  //   myFile.close();
  // } else {
  //   // if the file didn't open, print an error:
  //   Serial.println("error opening test.txt");
  // }
  delay(2000);
}



