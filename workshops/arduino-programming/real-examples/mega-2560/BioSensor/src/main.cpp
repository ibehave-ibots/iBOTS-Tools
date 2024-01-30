#include <Arduino.h>

const int numberOfLEDs = 5;
const int LEDArrayPins[] = {2,3,4,5,6};

const int Sensorpin = A0;

//int value = 0;
void setup() {
  for (byte i = 0; i < numberOfLEDs; i++){ // set LED pins as output
    pinMode(LEDArrayPins[i], OUTPUT);
  }
  pinMode(Sensorpin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // read value
  
  int value =  analogRead(Sensorpin); // read sensor
  
  // scale value to between 0 and 1
  const  int maxValue = 1024;
  const int minValue = 0;
  float scaledValue = (value - minValue)/float(maxValue);

  // determine number of LEDs to light
  int numberToLight = scaledValue * (numberOfLEDs + 1);

  // light up corresponging number of LEDs
  for (byte i = 0; i < numberOfLEDs; i++){ //loop over LEDs
    if (i < numberToLight){
      digitalWrite(LEDArrayPins[i], HIGH);
    }
    else{
      digitalWrite(LEDArrayPins[i], LOW);
    }
  }
  String debugLine = "value: " + String(value) + " scaledValue: " + String(scaledValue) + " numberToLight: " + String(numberToLight);
  Serial.println(debugLine);

  delay(100);
 }

//////////////////////////////////////////////////////////////////////////////



//IDUINO for Maker’s life
//www.openplatform.cc
int pulsePin = 0; // Pulse Sensor purple wire connected to analog pin 0
int blinkPin = 13; // pin to blink led at each beat
int fadePin = 5; // pin to do fancy classy fading blink at each beat
int fadeRate = 0; // used to fade LED on with PWM on
volatile int BPM; // used to hold the pulse rate
volatile int Signal; // holds the incoming raw data
volatile int IBI = 600; // holds the time between beats, the Inter-Beat Interval
volatile boolean Pulse = false; // true when pulse wave is high,false when it's low
volatile boolean QS = false; // becomes true when Arduoino finds a beat.


void setup(){
    pinMode(blinkPin,OUTPUT); // pin that will blink to your heartbeat!
    pinMode(fadePin,OUTPUT); // pin that will fade to your heartbeat!
    Serial.begin(115200); // we agree to talk fast!
    interruptSetup(); // sets up to read Pulse Sensor
}


void loop(){
  sendDataToProcessing('S', Signal); // send Processing the raw Pulse  Sensor data
  if (QS == true){ // Quantified Self flag is true  when arduino finds a heartbeat
    fadeRate = 255; // Set 'fadeRate' Variable to   255 to fade LED with pulse
    sendDataToProcessing('B',BPM); // send heart rate with a 'B'   prefix
    sendDataToProcessing('Q',IBI); // send time between beats with  a 'Q' prefix
    QS = false; // reset the Quantified Self   flag for next time
  }

  ledFadeToBeat();
  delay(20); // take a break
}


void ledFadeToBeat(){
  fadeRate -= 15; // set LED fade value
  fadeRate = constrain(fadeRate,0,255); // keep LED fade value from
  going into negative numbers!
  analogWrite(fadePin,fadeRate); // fade LED
}


void sendDataToProcessing(char symbol, int data ){
  Serial.print(symbol); // symbol prefix tells  Processing what type of data is coming
  Serial.println(data); // the data to send culminating  in a carriage return
}