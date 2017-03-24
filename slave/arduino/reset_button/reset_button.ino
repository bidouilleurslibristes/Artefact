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
void readInput();


int resetButton = 2;
char status;


long last_ping = 0;
BOOL connected = FALSE;

char ledPin = LED_BUILTIN;

void setupButton(){
  pinMode(resetButton, INPUT);
  digitalWrite(resetButton, INPUT_PULLUP); // connect internal pull-up
  status = 0;
}


void setup() {
  Serial.begin(115200);

  // Board LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  setupButton ();

  while (42) {
    main_loop();
  }
}


void scanButton();

void main_loop () {
  if (!connected) {
    connection();
  } else {
    if (millis() - last_ping > TIMEOUT)
      connected = FALSE;

    if (Serial.available())
      readInput();
    scanButton();
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
}


void scanButton(){
  int button_pressed = digitalRead(resetButton) == LOW;
  bool changed = false;

  if(button_pressed && status == 0) {
    changed = true;
    status = 1;
  }

  if(!button_pressed && status == 1) {
    changed = true;
    status = 0;
  }

  if (changed) {
    Serial.print("button-");
    Serial.print("0");
    Serial.print("-");
    if (button_pressed) {
      Serial.print("DOWN");
    } else {
      Serial.print("UP");
    }
    Serial.println();
    delay(30);
  }

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
