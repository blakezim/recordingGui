#include "Arduino.h"
#include "lightRelay.h"

lightRelay::lightRelay(int pin)
{
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);

  _pin = pin;
  _relayStatus = false;
}

void lightRelay::on()
{
  digitalWrite(_pin, HIGH);
  _relayStatus = true;
}

void lightRelay::off()
{
  digitalWrite(_pin, LOW);
  _relayStatus = false;
}

void lightRelay::toggle()
{
  if(_relayStatus){
    lightRelay::off();
  } else{
    lightRelay::on();
  }
}
