#include <EEPROM.h>

// 3 char ID
#define TRUE 42
#define FALSE (!42)
#define BOOL char

#define EEPROM_ID_ADDRESS 0
#define TIMEOUT 3000

// Functions definitions :
void connection ();


int button1_pressed = 0;

BOOL connected = FALSE;
long last_ping = 0;

char ledPin = LED_BUILTIN;
char ledPin2 = 10;
char button1Pin = 2;

void setupButtons(){
  pinMode(button1Pin, INPUT);
  digitalWrite(button1Pin, INPUT_PULLUP); // connect internal pull-up
}

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  digitalWrite(ledPin, LOW);
  digitalWrite(ledPin2, LOW);

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
   * 1C1C2C3C4... : LED STRIP COLORS, message starts with 1 followed by 32 led colors as defined in color.h => 33 bytes total
   * 2R1G1B1R2G2B2.... : LED BUTTON COLORS, message starts with 2 followed by 9*3 bytes for each led RGB color => 28 bytes total
   * 30/1 : SWAG BUTTON ON, message starts with 3 followed by "0" or "1" (resp off and on) => 2 bytes total
  */

  char firstChar = message.charAt(0);
  message.remove(0, 1);

   if(firstChar == '1'){
    setLedStripColor(message);
   }
   if(firstChar == '2'){
    setLedButtonsColor(message);
   }
   if(firstChar == '3'){
    setSwagButtonLed(message);
   }
}

void setLedButtonsColor(String message){
  digitalWrite(ledPin2, HIGH);
  Serial.println("led button color");

}

void setLedStripColor(String message){
  digitalWrite(ledPin2, LOW);
  Serial.println("strip color");
}

void setSwagButtonLed(String message){

}


void scanButtons(){

  if(button1_pressed == 1)
    button1_pressed = 0;
  else
    button1_pressed = 1;


  if (button1_pressed)
      digitalWrite(ledPin, HIGH);
  else
      digitalWrite(ledPin, LOW);

  Serial.print("button-");
  Serial.print(button1_pressed);
  Serial.println();
}


void pong () {
  String pong = "PONG !";

  connected = TRUE;

  if (connected) {
    Serial.println(pong);
    last_ping = millis();
  }

}
