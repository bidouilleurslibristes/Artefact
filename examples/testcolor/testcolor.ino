#include <Adafruit_NeoPixel.h>
#include "colorMacro.h"

#define pinRuban 3

int stripSize=32;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(stripSize,pinRuban, NEO_GRB);
uint16_t n;

void setup(){
  pinMode(pinRuban, OUTPUT);
  strip.begin();
}

void loop(){
  for(n=0;n<4;n++){
    strip.setPixelColor(n,yellow);
    strip.setPixelColor(n+4,green);
    strip.setPixelColor(n+8,cyan);
    strip.setPixelColor(n+12,blue);
    strip.setPixelColor(n+16,violet);
    strip.setPixelColor(n+20,white);
    strip.setPixelColor(n+24,red);
    strip.setPixelColor(n+28,orange);
    
  }
  strip.show();
}
