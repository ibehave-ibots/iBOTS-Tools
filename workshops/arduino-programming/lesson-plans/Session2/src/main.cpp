#include <Arduino.h>

const int redLED = 3;
const int greenLED = 4;
const int purpleLED = 5;

const int redBtn = 11;
const int greenBtn = 10;
const int purpleBtn = 9;

bool greenLEDon = false;

void setup() {
  pinMode(redLED, OUTPUT); 
  pinMode(greenLED, OUTPUT);
  pinMode(purpleLED, OUTPUT);

  pinMode(redBtn, INPUT_PULLUP);
  pinMode(greenBtn, INPUT_PULLUP);
  pinMode(purpleBtn, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
 
  Serial.println('hello!');
  delay(2000);

  int greenBtnState = digitalRead(greenBtn);
  // if (greenBtnState == LOW && greenLEDon == false ){
  //   digitalWrite(greenLED, HIGH); 
  //   greenLEDon = true;
  //   }
  // else if (greenBtnState == LOW && greenLEDon == true){
  //   digitalWrite(greenLED, LOW); 
  //   greenLEDon = false;
  // }
  delay(30);
  if (greenBtnState == LOW){
    if (greenLEDon == false){
       digitalWrite(greenLED, HIGH); 
       greenLEDon = true;
    }
    else {
       digitalWrite(greenLED, LOW); 
      greenLEDon = false;
      delay(30);
    }
  }

  }