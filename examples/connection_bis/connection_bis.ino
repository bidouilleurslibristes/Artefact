#include <EEPROM.h>

// 3 char ID
#define TRUE 42
#define FALSE (!42)
#define BOOL char

#define EEPROM_ID_ADDRESS 0

// Functions definitions :
void connection ();


BOOL connected = FALSE;
char ledPin = 13;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  connection();
}


void loop () {
  Serial.println("connected");
  delay (5000);
}

void connection () {
  connected = FALSE;
  char ARDUINO_ID = EEPROM.read(EEPROM_ID_ADDRESS);

  // Connection
  while (!connected) {
    // Send bonjour using the serial port
    Serial.print("BONJOUR ");
    Serial.println(ARDUINO_ID);
    
    if (Serial.available()) {
      char pc_response = Serial.read();
      
      if(pc_response == ARDUINO_ID)
        connected = TRUE;
    }
    
    Serial.println("CONNECTED");
  }
  
  // turn the LED on when connected
  digitalWrite(ledPin, HIGH);
}


void pong () {
  String str = "";
  String pong = "PONG";

  Serial.setTimeout(1000);
  str = Serial.readStringUntil('\n');
  
  if (str == NULL) {
    connected = FALSE; 
  } else {
    connected = pong.equals(str) ? TRUE : FALSE;
  }
}
