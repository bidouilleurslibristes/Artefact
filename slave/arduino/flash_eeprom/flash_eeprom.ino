#include <EEPROM.h>


void setup() {
  Serial.begin(9600);
  // initialize the LED pin as an output.
  pinMode(13, OUTPUT);
  // turn the LED on when we're done
  digitalWrite(13, LOW);

  char id = 42;
  int address = 0;

  if( EEPROM.read(address) != id ){
    EEPROM.write(address, id);
  }

  // turn the LED on when we're done
  digitalWrite(13, HIGH);
}

void loop() {
  Serial.println("caca");
  delay(1000);
}
