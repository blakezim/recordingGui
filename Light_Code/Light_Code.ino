#include "Arduino.h"
#include "lightRelay.h"

lightRelay LIGHT_0(13);
lightRelay LIGHT_1(12);

char serialInput ;

void setup() {
  Serial.begin(9600); //Initializing Arduino serial connection at a baud rate of 9600
}

void loop() {
  //empty until we decide we need to do something fancy
}

//serialEvent is what catches what you send from your python script
void serialEvent() {
  while (Serial.available()) {
    serialInput = Serial.read();
  }
  //Determine what to do given a serial command received
  switch (serialInput) {
    case 'a':
      LIGHT_0.on();
      LIGHT_1.off();
      break;
    case 'b':
      LIGHT_0.off();
      LIGHT_1.on();
      break;
    case 'c':
      LIGHT_0.off();
      LIGHT_1.off();
      break;
  }
  serialInput = ' '; //reset serial input character
}
