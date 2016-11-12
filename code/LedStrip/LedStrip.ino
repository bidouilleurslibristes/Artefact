#include <Adafruit_NeoPixel.h>
#define pinRuban 6

Adafruit_NeoPixel strip = Adafruit_NeoPixel(32, pinRuban, NEO_GRB);

uint32_t couleur[7];

void setup() {
  Serial.begin(9600);
  //randomSeed(analogRead(0));
  strip.begin();
  
  couleur[0] = strip.Color(00, 00, 00);// blanc
  couleur[1] = strip.Color(40, 01, 01);// rouge ok
  couleur[2] = strip.Color(01, 35, 02);// vert ok
  couleur[3] = strip.Color(02, 02, 50);// bleu ok
  couleur[4] = strip.Color(30, 28, 0);// jaune ok
  couleur[5] = strip.Color(30, 0, 40);// mauve ok
  couleur[6] = strip.Color(0, 35, 25);//turquoise ok
  couleur[7] = strip.Color(40,15,0);// orange ok
  couleur[8] = strip.Color(20,20,20);// blanc ok

  
  // Remise à zéro
  for (int led=0;led<32;led++){
    strip.setPixelColor(led,couleur[0]);
    strip.show();
  }
  delay(1000);
  strip.setPixelColor(5,couleur[1]);
  strip.show();
  delay(3000);
  
}
  
void loop() {
  
  for (int color = 0;color<8;color++){
    for (int i = 0;i<32;i++){
      strip.setPixelColor(i,couleur[color]);
      strip.show();
      delay(50);
    }
    delay(1000);
    for (int led=0;led<32;led++){
      strip.setPixelColor(led,couleur[0]);
      strip.show();
    }
  }

}
