#include <Adafruit_NeoPixel.h>

#define pinRuban 3

uint16_t stripSize=32;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(stripSize, pinRuban,NEO_GRB);
uint32_t couleur= 0x101050;

void setup() {
  pinMode(pinRuban, OUTPUT);
  strip.begin();
  for(uint16_t n=0; n<stripSize; n++){
    strip.setPixelColor(n,couleur);
  }
}

void loop(){
  strip.show();
  //for (int k=0; k<stripSize-1; k+=16)
  light_shutdown(0,stripSize,couleur);
  delay(100);
}

uint16_t i=0;
uint32_t contrast=0x050520;

void light_shutdown(uint16_t first_index, uint16_t last_index, uint32_t color){
  int j;
  if (i==0) j= last_index-first_index;
  else j=i-1;
  for (uint16_t k=first_index; k<=last_index;k++){
    if (k==first_index+i) strip.setPixelColor(k,color-contrast);
    else if (k==first_index+j) strip.setPixelColor(k,color+contrast);
    else strip.setPixelColor(k,color);
  }
  if (i==last_index-first_index) i=0;
  else i++;
}

