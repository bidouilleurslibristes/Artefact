#include <EEPROM.h>
#include <Adafruit_NeoPixel.h>
#include "Adafruit_TLC5947.h"

#define TRUE 42
#define FALSE (!42)
#define BOOL char

#define EEPROM_ID_ADDRESS 0
#define TIMEOUT 3000
#define LED_STRIP_IN 3

// Driver LED
#define NUM_TLC5974 1
#define data   4
#define clock   5
#define latch   6
#define oe  12
Adafruit_TLC5947 tlc = Adafruit_TLC5947(NUM_TLC5974, clock, data, latch);

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

// BUTTONS : 8 + swag
int buttons[9];
char buttonsStatus[9];
int swagLedPin = 2;

void initButtons() {
  buttons[0] = 8;
  buttons[1] = 9;
  buttons[2] = 10;
  buttons[3] = 11;
  buttons[4] = 12;
  buttons[5] = A0;
  buttons[6] = A1;
  buttons[7] = A2;
  buttons[8] = 7;
}


long last_ping = 0;
int button1_pressed = 0;

BOOL connected = FALSE;

char is_led_strip = TRUE;
char ledPin = LED_BUILTIN;

void setupButtons(){
  for (int i=0 ; i<9 ; i++) {
    pinMode(buttons[i], INPUT);
    digitalWrite(buttons[i], INPUT_PULLUP); // connect internal pull-up
    buttonsStatus[i] = 0;
  }
}

void setLedButtonsColor(String message);
void setSwagButtonLed(String message);
void setupDriver () {
  tlc.begin();
  if (oe >= 0) {
    pinMode(oe, OUTPUT);
    digitalWrite(oe, HIGH);
  }

  for (int led=0 ; led<8 ; led++) {
    tlc.setLED(led, 4095, 4095, 4095);
  }
  tlc.write();
  setLedButtonsColor("012345678");
  setSwagButtonLed("31");
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_STRIP_IN, INPUT_PULLUP);
  is_led_strip = digitalRead(LED_STRIP_IN) == LOW;

  // Board LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // Init
  initColors();
  if (is_led_strip) {
    strip.begin();
  } else {
    initButtons ();
    setupButtons ();
    setupDriver();
  }
}


void loop () {
  if (!connected) {
    connection();
  } else {
    if (millis() - last_ping > TIMEOUT)
      connected = FALSE;

    readInput();
    scanButtons();
  }
}


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

   if(firstChar == '1' && is_led_strip){
    setLedStripColor(message);
   }
   if(firstChar == '2' && !is_led_strip){
    setLedButtonsColor(message);
   }
   if(firstChar == '3' && !is_led_strip){
    setSwagButtonLed(message);
   }
}

void setLedButtonsColor(String message){
  // AC*8 (annimation + 8 colors (between 0 and 8))
  animation = message.charAt(0); // not used for now
  
  for (int i = 1;i<33;i++){
    int index = message.charAt(i) - '0';
    if(index < 0 || index > 8){
      Serial.println("bad color index ");
      Serial.print("index mess :");
      Serial.print(index); Serial.print(' ');
      Serial.println(message);
    }
    
    //buttonColors
    tlc.setLED(i-1, buttonColors[index][0],buttonColors[index][1],buttonColors[index][2]);
  }
  tlc.write();
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

void setSwagButtonLed(String message){
  if (message.charAt(1) == '0') {
    digitalWrite(swagLedPin, LOW);
  } else {
    digitalWrite(swagLedPin, HIGH);
  }
}

void scanButtons(){
  for (int i=0 ; i<8 ; i++) {
    int button_pressed = digitalRead(buttons[i]) == HIGH;
    int changed = FALSE;
    
    if(button_pressed && buttonsStatus[i] == 0) {
      changed = TRUE;
      buttonsStatus[i] = 1;
    }
    
    if(!button_pressed && buttonsStatus[i] == 1) {
      changed = TRUE;
      buttonsStatus[i] = 0;
    }

    if (changed) {
      Serial.print("button-");
      Serial.print(i);
      Serial.print("-");
      if (button_pressed) {
        Serial.print("UP");
      } else {
        Serial.print("DOWN");
      }
      Serial.println();
    }
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
