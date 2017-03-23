#include <Adafruit_NeoPixel.h>
#include "colorMacro.h"

#define r1 11
#define r2 4
#define r3 5
#define r4 6
#define r5 7
#define r6 8
#define r7 9
#define r8 10


int stripSize=32;
Adafruit_NeoPixel strip1 = Adafruit_NeoPixel(stripSize,r1, NEO_GRB);
Adafruit_NeoPixel strip2 = Adafruit_NeoPixel(stripSize,r2, NEO_GRB);
Adafruit_NeoPixel strip3 = Adafruit_NeoPixel(stripSize,r3, NEO_GRB);
Adafruit_NeoPixel strip4 = Adafruit_NeoPixel(stripSize,r4, NEO_GRB);
Adafruit_NeoPixel strip5 = Adafruit_NeoPixel(stripSize,r5, NEO_GRB);
Adafruit_NeoPixel strip6 = Adafruit_NeoPixel(stripSize,r6, NEO_GRB);
Adafruit_NeoPixel strip7 = Adafruit_NeoPixel(stripSize,r7, NEO_GRB);
Adafruit_NeoPixel strip8 = Adafruit_NeoPixel(stripSize,r8, NEO_GRB);
uint16_t n;

void setup(){
  pinMode(r1, OUTPUT);
  strip1.begin();
   pinMode(r2, OUTPUT);
  strip2.begin();
   pinMode(r3, OUTPUT);
  strip3.begin();
   pinMode(r4, OUTPUT);
  strip4.begin();
   pinMode(r5, OUTPUT);
  strip5.begin();
   pinMode(r6, OUTPUT);
  strip6.begin();
   pinMode(r7, OUTPUT);
  strip7.begin();
   pinMode(r8, OUTPUT);
  strip8.begin();
}

void loop(){
  for(n=0;n<32;n++){
    strip1.setPixelColor(n,toto);
    strip2.setPixelColor(n,toto);
    strip3.setPixelColor(n,toto);
    strip4.setPixelColor(n,toto);
    strip5.setPixelColor(n,toto);
    strip6.setPixelColor(n,toto);
    strip7.setPixelColor(n,toto);
    strip8.setPixelColor(n,toto);
  }
  strip1.show();
  strip2.show();
  strip3.show();
  strip4.show();
  strip5.show();
  strip6.show();
  strip7.show();
  strip8.show();
}
