#include <Arduino.h>
#include <CapacitiveSensor.h>


CapacitiveSensor   cs_7_8 = CapacitiveSensor(49,51);        // 10 megohm resistor between pins 4 & 2, pin 2 is sensor pin, add wire, foil

unsigned long csSum;

void setup() {
    Serial.begin(9600);
}



void CSread() {
    long cs = cs_7_8.capacitiveSensor(80); //a: Sensor resolution is set to 80
	if (cs > 100) { //b: Arbitrary number
		csSum += cs;
		Serial.println(cs); 
		if (csSum >= 3800) //c: This value is the threshold, a High value means it takes longer to trigger
		{
			Serial.print("Trigger: ");
			Serial.println(csSum);
			if (csSum > 0) { csSum = 0; } //Reset
			cs_7_8.reset_CS_AutoCal(); //Stops readings
		}
	} else {
		csSum = 0; //Timeout caused by bad readings
	}
}
void loop() {
    CSread();
}