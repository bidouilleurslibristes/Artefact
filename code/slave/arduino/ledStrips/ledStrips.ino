#include <EEPROM.h>
#include <Adafruit_NeoPixel.h>
#include "Adafruit_TLC5947.h"
#include "Color.h"

#define TRUE 42
#define FALSE (!42)
#define BOOL char

#define EEPROM_ID_ADDRESS 0
#define TIMEOUT 100000


// Functions definitions :
void connection ();

// LED STRIP
int pinsRuban[8] = {
  4, 5, 6, 7,   // led strips 0, 1, 2, 3
  8, 9, 10, 11  // led strips 4, 5, 6, 7
};

//Adafruit_NeoPixel _a = Adafruit_NeoPixel(32, 4, NEO_GRB);
//Adafruit_NeoPixel _b = Adafruit_NeoPixel(32, 5, NEO_GRB);

Adafruit_NeoPixel strips[8] = {
  Adafruit_NeoPixel(32, 4, NEO_GRB),
  Adafruit_NeoPixel(32, 5, NEO_GRB),
  Adafruit_NeoPixel(32, 6, NEO_GRB),
  Adafruit_NeoPixel(32, 7, NEO_GRB),
  Adafruit_NeoPixel(32, 8, NEO_GRB),
  Adafruit_NeoPixel(32, 9, NEO_GRB),
  Adafruit_NeoPixel(32, 10, NEO_GRB),
  Adafruit_NeoPixel(32, 11, NEO_GRB)
};

void initStrips(){
  for(int i = 0; i < 8; i++){
    //strips[i] = Adafruit_NeoPixel(32, pinsRuban[i], NEO_GRB);
    strips[i].begin();
  }
  //_a.begin();
  //_b.begin();
}

int freeRam () {
  extern int __heap_start, *__brkval;
  int v;
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
}

uint32_t colors[9];
void initColors(){
  colors[0] = Adafruit_NeoPixel::Color(00, 00, 00);// noir
  colors[1] = Adafruit_NeoPixel::Color(40, 01, 01);// rouge ok
  colors[2] = Adafruit_NeoPixel::Color(01, 35, 02);// vert ok
  colors[3] = Adafruit_NeoPixel::Color(02, 02, 50);// bleu ok
  colors[4] = Adafruit_NeoPixel::Color(30, 28, 0);// jaune ok
  colors[5] = Adafruit_NeoPixel::Color(30, 0, 40);// mauve ok
  colors[6] = Adafruit_NeoPixel::Color(0, 35, 25);//turquoise ok
  colors[7] = Adafruit_NeoPixel::Color(40,15,0);// orange ok
  colors[8] = Adafruit_NeoPixel::Color(20,20,20);// blanc ok
}


long last_ping = 0;
int button1_pressed = 0;

bool connected = false;
char ledPin = LED_BUILTIN;

void setup() {
  Serial.begin(115200);

  // Board LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);

  // Init
  initStrips();
  initColors();
  for(int i=0;i<8;i++){
    //Serial.print("set color strip : ") ; Serial.println(i);
    strips[i].setPixelColor(6,255,255,255);
    strips[i].show();
  }

  delay(1000);
  digitalWrite(ledPin, LOW);
  
  while (42) {
    main_loop();
  }
}


void main_loop () {
  if (!connected) {
    connection();
  } else {
    if (millis() - last_ping > TIMEOUT)
      connected = FALSE;

    if (Serial.available())
      readInput();
  }
}

void loop () {}


void connection () {
  Serial.flush();

  connected = FALSE;
  char ARDUINO_ID = EEPROM.read(EEPROM_ID_ADDRESS);

  // Connection
  while (!connected) {
    // Send bonjour using the serial port
    if (Serial.available()) {
      String str = Serial.readString();
      int val = str.toInt();

      if(val == ARDUINO_ID)
        connected = TRUE;
    } else {
      Serial.print("BONJOUR ");
      Serial.println((int)ARDUINO_ID);
      delay(500);
    }
  }
  Serial.flush();
  Serial.println("CONNECTED");
  Serial.flush();

  // turn the LED on when connected
  //digitalWrite(ledPin, HIGH);
  last_ping = millis();
}


void readInput(){
  String str = "";
  String ping = "PING ?";

  str = Serial.readStringUntil('\n');

  if (ping.equals(str))
    pong();
  else{
    parseMessage(str);
  }
}

void parseMessage(String message){
  /*
  Protocol :
   * 1ANC1C2C3C4...C32 : LED STRIP COLORS, message starts with 1 followed by the strip ID, by 32 led colors as defined in color.h => 34 bytes total
  */

  char firstChar = message.charAt(0);
  message.remove(0, 1);

   if(firstChar == '1'){
    setLedStripColor(message);
   }
   else if(firstChar == '2'){
    setEndAnimation(message);
   }
   else if(firstChar == '3'){
    setFadeOut(message);
   }
}

void setFadeOut(String message){
  /*
   Set a fade out on all strips during 2.5s
   Starts from green.
  */

   Color green = Color(01, 35, 02);
   Color green2;
   double factor = 0.97; // magic, do not touch, brightness is multipied by this
   double cumulatedFactor = factor;
   for(int i = 0; i < 100; i++){
    cumulatedFactor *= factor;
    green2 = green.multiplyLum(cumulatedFactor, 1);
    setAllLedStrips(green2.red, green2.green, green2.blue);
    delay(25);
    Serial.print(green2.red);Serial.print(" ");Serial.print(green2.green);Serial.print(" ");Serial.println(green2.blue);
   }
   setAllLedStrips(0, 0, 0);
}

void setAllLedStrips(int r, int g, int b){
   for(int s = 0; s < 8; s++){
     for(int p = 0; p < 32; p++){
      strips[s].setPixelColor(p, r, g, b);
     }
     strips[s].show();
   }
}

void setEndAnimation(String message){
  /*
   Set a fade out on all strips during 2.5s
   Starts from green.
   */

   Color green = Color(01, 35, 02);
   Color green2;
   double factor = 1.02; // magic, do not touch, brightness is multipied by this
   double cumulatedFactor = factor;
   for(int i = 0; i < 150; i++){
    cumulatedFactor *= factor;
    green2 = green.multiplyLum(cumulatedFactor, 0.9); // color luminosity is capped 
    setAllLedStrips(green2.red, green2.green, green2.blue);
    //Serial.print(green2.red);Serial.print(" ");Serial.print(green2.green);Serial.print(" ");Serial.println(green2.blue);
    delay(35);
   }
   endFlicker();
}


#define NB_STEPS 100
void endFlicker(){
  byte colors[8][32];
  for(int step=0; step < NB_STEPS; step++){
    delay(15);
    //byte currentLuminosity = (byte) (255.0 - (step * 1.0) / NB_STEPS);
    double threshold = ((double)(NB_STEPS - step) / NB_STEPS) * 100;

    for(int strip=0; strip < 8; strip++){
      for(int led=0; led < 32; led++){
        int proba = random(100);
        colors[strip][led] = 0;
        if(proba < threshold)
          colors[strip][led] = 100;
        //Serial.print(proba); Serial.print(" "); Serial.print(threshold); Serial.print(" -> "); Serial.println(colors[strip][led]);
      }
    }


    for(int strip=0; strip < 8; strip++){
      for(int led=0; led < 32; led++){
        strips[strip].setPixelColor(led, colors[strip][led], colors[strip][led], colors[strip][led]);
      }
      strips[strip].show();
    }
  }

  setAllLedStrips(0, 0, 0);
}


void setLedStripColor(String message){
  // AIC*32 (annimation + 32 colors (between 0 and 8))
  char animation;
  int strip_id;

  animation = message[0]; // not used for now
  strip_id = message[1] - '0';

  for (int i = 2;i<34;i++){
    int index = message[i] - '0';
    if(index < 0 || index > 8){
      Serial.println("bad color index ");

      Serial.print("i : ") ; Serial.print(i) ;
      Serial.print(" -- charAt i : ") ;
      Serial.print(message[i]);
      Serial.print("  -- index mess :");
      Serial.print(index);
      Serial.print(' ');
      Serial.println(message);
      return;
    }
    uint32_t color = colors[index];
    strips[strip_id].setPixelColor(i-2, color);
  }

  for(int i=0; i<8; i++){
    //Serial.print("Show Strip : "); Serial.println(i);
    strips[i].show();
  }
}


void pong () {
  String pong = "PONG !";

  connected = TRUE;

  if (connected) {
    Serial.println(pong);
    last_ping = millis();
  }

}
