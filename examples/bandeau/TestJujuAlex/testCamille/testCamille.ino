#include <Adafruit_NeoPixel.h>

#define pinRuban 3

int stripSize=32;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(stripSize, pinRuban, NEO_GRB);
uint32_t couleur[8];
uint16_t n;

void setup() {
  pinMode(pinRuban, OUTPUT);
  strip.begin();
  couleur[0] = strip.Color(40, 01, 01);// rouge ok
  couleur[1] = strip.Color(01, 35, 02);// vert ok
  couleur[2] = strip.Color(02, 02, 50);// bleu ok
  couleur[3] = strip.Color(30, 28, 0);// jaune ok
  couleur[4] = strip.Color(30, 0, 40);// mauve ok
  couleur[5] = strip.Color(0, 35, 25);//turquoise ok
  couleur[6] = strip.Color(40,15,0);// orange ok
  couleur[7] = strip.Color(20,20,20);// blanc ok
}

void loop() {
  for(n=0;n<stripSize;n++){
    strip.setPixelColor(n,couleur[2]);
  }
  strip.show();
  delay(50);
}
