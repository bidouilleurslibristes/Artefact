#include <EEPROM.h>

#define TRUE 42
#define FALSE (!42)
#define BOOL char

#define EEPROM_ID_ADDRESS 0
#define TIMEOUT 5000


// Functions definitions :
void connection ();
void readInput();


int easyButton = 2;
int normalButton = 3;
int hardButton = 4;

char status[5] = {0, 0, 0, 0, 0};

long last_ping = 0;
BOOL connected = FALSE;

char ledPin = LED_BUILTIN;

void setupButton(){
  pinMode(easyButton, INPUT);
  digitalWrite(easyButton, INPUT_PULLUP); // connect internal pull-up
  pinMode(normalButton, INPUT);
  digitalWrite(normalButton, INPUT_PULLUP); // connect internal pull-up
  pinMode(hardButton, INPUT);
  digitalWrite(hardButton, INPUT_PULLUP); // connect internal pull-up
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
    scanAllButton();
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

bool scanButton(int pin, int* button_pressed) {
  button_pressed = digitalRead(pin) == LOW;
  bool changed = false;

  if(button_pressed && status[pin] == 0) {
    changed = true;
    status[pin] = 1;
  }

  if(!button_pressed && status[pin] == 1) {
    changed = true;
    status[pin] = 0;
  }

  return changed;
}

void scanAllButton(){
  String button = "-";
  int button_pressed = 0;
  
  if (scanButton(easyButton, &button_pressed)) {
    button = "0";
  } else if (scanButton(normalButton, &button_pressed)) {
    button = "1";
  } else if (scanButton(hardButton, &button_pressed)) {
    button = "2";
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

  connected = TRUE;

  if (connected) {
    Serial.println(pong);
    last_ping = millis();
  }

}
