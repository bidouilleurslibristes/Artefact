/*************************************************** 
  This is an example for our Adafruit 24-channel PWM/LED driver

  Pick one up today in the adafruit shop!
  ------> http://www.adafruit.com/products/1429

  These drivers uses SPI to communicate, 3 pins are required to  
  interface: Data, Clock and Latch. The boards are chainable

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include "Adafruit_TLC5947.h"

// How many boards do you have chained?
#define NUM_TLC5974 1

#define data   4
#define clock   5
#define latch   6
#define oe  12  // set to -1 to not use the enable pin (its optional)
/**/

Adafruit_TLC5947 tlc = Adafruit_TLC5947(NUM_TLC5974, clock, data, latch);

void setup() {
  Serial.begin(9600);
  
  Serial.println("TLC5974 test");
  tlc.begin();
  if (oe >= 0) {
    pinMode(oe, OUTPUT);
    digitalWrite(oe, HIGH);
  }
}

void loop() {
  /**
  colorWipe(4095, 0, 0, 100); // "Red" (depending on your LED wiring)
  delay(200);
  colorWipe(0, 4095, 0, 100); // "Green" (depending on your LED wiring)
  delay(200);
  colorWipe(0, 0, 4095, 100); // "Blue" (depending on your LED wiring)
  delay(200);
  rainbowCycle(10);
  */
  delay(80);
  tlc.setPWM(9, 4095);
  tlc.setPWM(11, 0);
  tlc.setPWM(12, 4095);
  tlc.setPWM(13, 0);
  tlc.write();
  delay(80);
  tlc.setPWM(11, 4095);
  tlc.setPWM(9, 0);
  tlc.setPWM(12, 0);
  tlc.setPWM(13, 4095);
  tlc.write();
}  


// Fill the dots one after the other with a color
void colorWipe(uint16_t r, uint16_t g, uint16_t b, uint8_t wait) {
  for(uint16_t i=0; i<8*NUM_TLC5974; i++) {
      tlc.write();
      delay(wait);
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint32_t i, j;

  for(j=0; j<4096; j++) { // 1 cycle of all colors on wheel
    for(i=0; i< 8*NUM_TLC5974; i++) {
      Wheel(i, ((i * 4096 / (8*NUM_TLC5974)) + j) & 4095);
    }
    tlc.write();
    delay(wait);
  }
}

// Input a value 0 to 4095 to get a color value.
// The colours are a transition r - g - b - back to r.
void Wheel(uint8_t ledn, uint16_t WheelPos) {
  if(WheelPos < 1365) {
    tlc.setLED(ledn, 3*WheelPos, 4095 - 3*WheelPos, 0);
  } else if(WheelPos < 2731) {
    WheelPos -= 1365;
    tlc.setLED(ledn, 4095 - 3*WheelPos, 0, 3*WheelPos);
  } else {
    WheelPos -= 2731;
    tlc.setLED(ledn, 0, 3*WheelPos, 4095 - 3*WheelPos);
  }
}
