#include <EEPROM.h>
#include <Adafruit_NeoPixel.h>
#include "Adafruit_TLC5947.h"

#define TRUE 42
#define FALSE (!42)
#define BOOL char

#define EEPROM_ID_ADDRESS 0
#define TIMEOUT 300000
#define LED_STRIP_IN 3


// Functions definitions :
void connection ();

// LED STRIP
int pinRuban = 6;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(32, pinRuban, NEO_GRB);

char animation;
uint32_t colors[9];
int buttonColors[9][3] = {
  {4095,4095,4095}, // noir
  {0,4095,4095}, // Rouge
  {4095,0,4095}, // vert
  {4095,4095,0}, // bleu
  {0,2200,4095}, // Jaune
  {0,4095,0}, // Mauve
  {4095,0,0}, //Cyan
  {0,3500,4095}, // Orange
  {0,0,0} // Blanc
};

void initColors(){
  colors[0] = strip.Color(00, 00, 00);// noir
  colors[1] = strip.Color(40, 01, 01);// rouge ok
  colors[2] = strip.Color(01, 35, 02);// vert ok
  colors[3] = strip.Color(02, 02, 50);// bleu ok
  colors[4] = strip.Color(30, 28, 0);// jaune ok
  colors[5] = strip.Color(30, 0, 40);// mauve ok
  colors[6] = strip.Color(0, 35, 25);//turquoise ok
  colors[7] = strip.Color(40,15,0);// orange ok
  colors[8] = strip.Color(20,20,20);// blanc ok
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
  initColors();
  strip.begin();

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
   * 1AC1C2C3C4... : LED STRIP COLORS, message starts with 1 followed by 32 led colors as defined in color.h => 33 bytes total
   * 2R1G1B1R2G2B2.... : LED BUTTON COLORS, message starts with 2 followed by 9*3 bytes for each led RGB color => 28 bytes total
   * 30/1 : SWAG BUTTON ON, message starts with 3 followed by "0" or "1" (resp off and on) => 2 bytes total
  */

  char firstChar = message.charAt(0);
  message.remove(0, 1);

   if(firstChar == '1'){
    setLedStripColor(message);
   }
}

void setLedStripColor(String message){
  // AC*32 (annimation + 32 colors (between 0 and 8))
  animation = message.charAt(0); // not used for now
  
  for (int i = 1;i<33;i++){
    int index = message.charAt(i) - '0';
    if(index < 0 || index > 8){
      Serial.println("bad color index ");
      Serial.print("index mess :");
      Serial.print(index); Serial.print(' ');
      Serial.println(message);
    }

    uint32_t color = colors[index];

    strip.setPixelColor(i, color);
  }
  strip.show();
}


void pong () {
  String pong = "PONG !";

  connected = TRUE;

  if (connected) {
    Serial.println(pong);
    last_ping = millis();
  }

}
