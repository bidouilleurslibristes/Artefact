#include <EEPROM.h>
#include <Adafruit_NeoPixel.h>
#include "Adafruit_TLC5947.h"

#define TRUE 42
#define FALSE (!42)
#define BOOL char

#define EEPROM_ID_ADDRESS 0
#define TIMEOUT 5000


// Functions definitions :
void connection ();

// LED buttons
int pinRuban = 6;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(8, pinRuban, NEO_GRB);

uint32_t colors[9];

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
  buttons[0] = A0;
  buttons[1] = A1;
  buttons[2] = A2;
  buttons[3] = A3;
  buttons[4] = A4;
  buttons[5] = A5;
  buttons[6] = 8;
  buttons[7] = 9;
  buttons[8] = 10;
}


long last_ping = 0;
int button1_pressed = 0;

BOOL connected = FALSE;

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

void setup() {
  Serial.begin(115200);

  // Board LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  strip.begin();
  initButtons ();
  initColors ();
  setupButtons ();

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
    scanButtons();
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

   * 11AC1C2C3C4... : LED STRIP COLORS, message starts with 1 followed by the strip ID, by 32 led colors as defined in color.h => 34 bytes total
   * 2C1C2C3.... : LED BUTTON COLORS, message starts with 2 followed by 8 bytes for each led RGB color => 9 bytes total
   * 30/1 : SWAG BUTTON ON, message starts with 3 followed by "0" or "1" (resp off and on) => 2 bytes total
  */

  char firstChar = message.charAt(0);
  message.remove(0, 1);

  if(firstChar == '2'){
    setLedButtonsColor(message);
  } else if(firstChar == '3'){
    setSwagButtonLed(message);
  }
}

void setLedButtonsColor(String message){
  for (int i = 0;i<8;i++){
    char c = message[i];
    int index = (int)(c - '0');
    if(index < 0 || index > 8){
      Serial.println("bad color index ");
      Serial.print("index mess :");
      Serial.print(index); Serial.print(' ');
      Serial.println(message);
      continue;
    }

    //buttonColors
    uint32_t color = colors[index];
    strip.setPixelColor(i, color);
  }
  strip.show();
}

void setSwagButtonLed(String message){
  if (message[0] == '0') {
    digitalWrite(swagLedPin, LOW);
  } else if (message[0] == '1') {
    digitalWrite(swagLedPin, HIGH);
  }
}

void scanButtons(){
  bool meta_changed = false;

  for (int i=0 ; i<9 ; i++) {
    int button_pressed = digitalRead(buttons[i]) == LOW;
    bool changed = false;

    if(button_pressed && buttonsStatus[i] == 0) {
      changed = true;
      buttonsStatus[i] = 1;
    }

    if(!button_pressed && buttonsStatus[i] == 1) {
      changed = true;
      buttonsStatus[i] = 0;
    }

    if (changed) {
      meta_changed = true;
      Serial.print("button-");
      Serial.print(i);
      Serial.print("-");
      if (button_pressed) {
        Serial.print("DOWN");
      } else {
        Serial.print("UP");
      }
      Serial.println();
    }
  }

  if (meta_changed)
    delay(30);

   delay(5);
}


void pong () {
  String pong = "PONG !";

  connected = TRUE;

  if (connected) {
    Serial.println(pong);
    last_ping = millis();
  }

}
