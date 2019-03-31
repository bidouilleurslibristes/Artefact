#include <EEPROM.h>

#define EEPROM_ID_ADDRESS 0
#define TIMEOUT 5000


// Functions definitions :
void connection ();
void readInput();
void scanButton();
void scanAllButtons();


int easyButton = 2;
int normalButton = 3;
int hardButton = 4;

int easyLed = 8;
int normalLed = 9;
int hardLed = 10;

char status[5] = {1, 1, 1, 1, 1};

long last_ping = 0;
bool connected = false;

char ledPin = LED_BUILTIN;

void setupButton(){
  pinMode(easyButton, INPUT);
  digitalWrite(easyButton, INPUT_PULLUP); // connect internal pull-up
  
  pinMode(normalButton, INPUT);
  digitalWrite(normalButton, INPUT_PULLUP); // connect internal pull-up
  
  pinMode(hardButton, INPUT);
  digitalWrite(hardButton, INPUT_PULLUP); // connect internal pull-up
}

void setupLed(){
    pinMode(easyLed, OUTPUT);
    pinMode(normalLed, OUTPUT);
    pinMode(hardLed, OUTPUT);
}

void setup() {
  Serial.begin(115200);

  // Board LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  setupButton();
  setupLed();
}


void loop() {
  if (!connected) {
    connection();
  } 
  else {
    if (millis() - last_ping > TIMEOUT)
      connected = false;

    if (Serial.available())
      readInput();


    scanAllButtons();
  }
}


void connection () {
  Serial.flush();

  connected = false;
  char ARDUINO_ID = EEPROM.read(EEPROM_ID_ADDRESS);

  // Connection
  while (!connected) {
    // Send bonjour using the serial port
    if (Serial.available()) {
      String str = Serial.readString();
      int val = str.toInt();

      if(val == ARDUINO_ID)
        connected = true;
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

bool scanButton(int pin, bool* button_pressed) {
  *button_pressed = (digitalRead(pin) == HIGH);
  bool changed = false;

  if(*button_pressed && status[pin] == 0) {
    changed = true;
    status[pin] = 1;
  }

  if(!*button_pressed && status[pin] == 1) {
    changed = true;
    status[pin] = 0;
  }

  if(changed)
    lighLedForButton(pin);
  
  return changed;
}

void allLedOff(){
  digitalWrite(easyLed, LOW);
  digitalWrite(normalLed, LOW);
  digitalWrite(hardLed, LOW);
}

void lighLedForButton(int buttonPin){
  allLedOff();
  if(buttonPin == easyButton){
    digitalWrite(easyLed, HIGH);
  }
  else if (buttonPin == normalButton){
    digitalWrite(normalLed, HIGH);
  }
  else if (buttonPin == hardButton){
    digitalWrite(hardLed, HIGH);
  }
  else{
  }
}

void scanAllButtons(){
  String button = "-";
  bool button_pressed = 0;
  
  if (scanButton(easyButton, &button_pressed)) {
    button = "easy";
  } else if (scanButton(normalButton, &button_pressed)) {
    button = "normal";
  } else if (scanButton(hardButton, &button_pressed)) {
    button = "hard";
  }
  
  if (button != "-") {
    Serial.print("button-");
    Serial.print(button);
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

  connected = true;

  if (connected) {
    Serial.println(pong);
    last_ping = millis();
  }

}
