#include <EEPROM.h>

int address = 0;
byte idValue = 0;
byte value;


void setup(){
   
  Serial.begin(9600);
  while(!Serial){;}
    
  value = EEPROM.read(address);
  
  Serial.print(address);
  Serial.print("\t");
  Serial.print(value, DEC);
  Serial.println();
}

void loop(){
}
