#include <Arduino.h>

import processing.serial.*;
Serial mySerial;
PrintWriter output;
void setup() {
   mySerial = new Serial( this, Serial.list()[0], 9600 );
   output = createWriter( "newp.txt" );
   //print(Serial.list());
}
void draw() {
    if (mySerial.available() > 0 ) {
         String value = mySerial.readString();
         if ( value != null ) {
              output.println( value );
               output.close();
             

         }
    }
 
}
