#include <Adafruit_NeoPixel.h>
#define pinRuban 6

Adafruit_NeoPixel strip = Adafruit_NeoPixel(15, pinRuban, NEO_GRB);

uint32_t couleur[7];
int intensite = 35;

void setup() {
  Serial.begin(9600);
  //randomSeed(analogRead(0));
  strip.begin();
  couleur[0] = strip.Color(intensite, 0, 0);
  couleur[1] = strip.Color(0, intensite, 0);
  couleur[2] = strip.Color(0, 0, intensite);
  couleur[3] = strip.Color(intensite, intensite, 0);
  couleur[4] = strip.Color(intensite, 0, intensite);
  couleur[5] = strip.Color(0, intensite, intensite);
  couleur[6] = strip.Color(intensite, intensite, intensite);
}

void loop() {

    if(Serial.available()>=15){
      for (int i = 0; i < 15; i++) {
        char info = Serial.read();
        Serial.println(info);
        strip.setPixelColor(i, couleur[info]);
        strip.show();
      }
    }

    delay(1000);
}
