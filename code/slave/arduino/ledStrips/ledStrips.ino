#include <EEPROM.h>
#include <Adafruit_NeoPixel.h>
#include "Adafruit_TLC5947.h"

#define TRUE 42
#define FALSE (!42)
#define BOOL char

#define EEPROM_ID_ADDRESS 0
#define TIMEOUT 10000


// Functions definitions :
void connection ();

// LED STRIP
int pinsRuban[8] = {
  4, 5, 6, 7,   // led strips 0, 1, 2, 3
  8, 9, 10, 11  // led strips 4, 5, 6, 7
};
Adafruit_NeoPixel strips[8];

void initStrips(){
  for(int i = 0; i < 8; i++){
    Adafruit_NeoPixel strip = Adafruit_NeoPixel(32, pinsRuban[i], NEO_GRB);
    strips[i] = strip;
    strip.begin();
  }
}


uint32_t colors[9];
void initColors(){
  colors[0] = strips[0].Color(00, 00, 00);// noir
  colors[1] = strips[0].Color(40, 01, 01);// rouge ok
  colors[2] = strips[0].Color(01, 35, 02);// vert ok
  colors[3] = strips[0].Color(02, 02, 50);// bleu ok
  colors[4] = strips[0].Color(30, 28, 0);// jaune ok
  colors[5] = strips[0].Color(30, 0, 40);// mauve ok
  colors[6] = strips[0].Color(0, 35, 25);//turquoise ok
  colors[7] = strips[0].Color(40,15,0);// orange ok
  colors[8] = strips[0].Color(20,20,20);// blanc ok
}


long last_ping = 0;
int button1_pressed = 0;

bool connected = false;
char ledPin = LED_BUILTIN;

void setup() {
  Serial.begin(115200);

  // Board LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // Init
  initStrips();
  initColors();

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
  digitalWrite(ledPin, HIGH);
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
   * 1NAC1C2C3C4...C32 : LED STRIP COLORS, message starts with 1 followed by the strip ID, by 32 led colors as defined in color.h => 34 bytes total
  */

  char firstChar = message.charAt(0);
  message.remove(0, 1);

   if(firstChar == '1'){
    setLedStripColor(message);
   }
}

void setLedStripColor(String message){
  // AC*32 (annimation + 32 colors (between 0 and 8))
  char animation;
  int strip_id;

  animation = message.charAt(0); // not used for now
  strip_id = message.charAt(1) - '0';

  for (int i = 2;i<33;i++){
    int index = message.charAt(i) - '0';

    if(index < 0 || index > 8){
      Serial.println("bad color index ");
      Serial.print("index mess :");
      Serial.print(index); Serial.print(' ');
      Serial.println(message);
    }

    uint32_t color = colors[index];

    strips[strip_id].setPixelColor(i, color);
  }
  strips[strip_id].show();
}


void pong () {
  String pong = "PONG !";

  connected = TRUE;

  if (connected) {
    Serial.println(pong);
    last_ping = millis();
  }

}
