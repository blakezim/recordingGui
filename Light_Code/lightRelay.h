#ifndef lightRelay_h
#define lightRelay_h

#include "Arduino.h"

class lightRelay
{
  public:
    lightRelay(int pin);
    void on();
    void off();
    void toggle();
  private:
    int _pin;
    bool _relayStatus;
};

#endif
