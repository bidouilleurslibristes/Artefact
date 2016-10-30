#include <EEPROM.h>

void setup() {
  // initialize the LED pin as an output.
  pinMode(13, OUTPUT);
  // turn the LED on when we're done
  digitalWrite(13, LOW);

  char id = {{ ID }};
  int address = 0;

  if( EEPROM.read(address) != id ){
    EEPROM.write(address, id);
  }

  // turn the LED on when we're done
  digitalWrite(13, HIGH);
}

void loop() {
  /** Empty loop. **/
}