#include <EEPROM.h>

// 3 char ID
#define TRUE 42
#define FALSE (!42)
#define BOOL char

#define EEPROM_ID_ADDRESS 0
#define TIMEOUT 3000

// Functions definitions :
void connection ();


BOOL connected = FALSE;
char ledPin = 13;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}


void loop () {
  if (!connected) {
    connection();
  } else
    pong();

  // Insert functions calls here to do things between two pings
}


long last_ping = 0;

void connection () {
  connected = FALSE;
  char ARDUINO_ID = EEPROM.read(EEPROM_ID_ADDRESS);

  // Connection
  while (!connected) {
    // Send bonjour using the serial port
    Serial.print("BONJOUR ");
    Serial.println((int)ARDUINO_ID);
    
    if (Serial.available()) {
      char pc_response = (char) Serial.parseInt();
      
      if(pc_response == ARDUINO_ID)
        connected = TRUE;
    } else
      delay(1000);
  }
  Serial.println("CONNECTED");
  
  // turn the LED on when connected
  digitalWrite(ledPin, HIGH);
  last_ping = millis();
}


void pong () {
  String str = "";
  String ping = "PING ?";
  String pong = "PONG !";

  // In case of no new data
  if (!Serial.available()) {
    if (millis() - last_ping > TIMEOUT)
      connected = FALSE;
    return;
  }

  // In case of new data
  str = Serial.readStringUntil('\n');
  connected = ping.equals(str) ? TRUE : FALSE;
  if (connected) {
    Serial.println(pong);
    last_ping = millis();
  }
}
