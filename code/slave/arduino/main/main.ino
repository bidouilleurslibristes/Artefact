#include <EEPROM.h>
#include <Adafruit_NeoPixel.h>

#define TRUE 42
#define FALSE (!42)
#define BOOL char

#define EEPROM_ID_ADDRESS 0
#define TIMEOUT 3000
#define LED_STRIP_IN 3

// Functions definitions :
void connection ();

// LED STRIP
int pinRuban = 6;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(32, pinRuban, NEO_GRB);

char animation;
uint32_t colors[9];

void initColors(){
  colors[0] = strip.Color(00, 00, 00);// blanc
  colors[1] = strip.Color(40, 01, 01);// rouge ok
  colors[2] = strip.Color(01, 35, 02);// vert ok
  colors[3] = strip.Color(02, 02, 50);// bleu ok
  colors[4] = strip.Color(30, 28, 0);// jaune ok
  colors[5] = strip.Color(30, 0, 40);// mauve ok
  colors[6] = strip.Color(0, 35, 25);//turquoise ok
  colors[7] = strip.Color(40,15,0);// orange ok
  colors[8] = strip.Color(20,20,20);// blanc ok
}

// BUTTONS
int buttons[8];

void initButtons() {
  buttons[0] = 8;
  buttons[1] = 9;
  buttons[2] = 10;
  buttons[3] = 11;
  buttons[4] = 12;
  buttons[5] = A0;
  buttons[6] = A1;
  buttons[7] = A2;
}


long last_ping = 0;
int button1_pressed = 0;

BOOL connected = FALSE;

char is_led_strip = TRUE;
char ledPin = LED_BUILTIN;

void setupButtons(){
  for (int i=0 ; i<8 ; i++) {
    pinMode(buttons[i], INPUT);
    digitalWrite(buttons[i], INPUT_PULLUP); // connect internal pull-up
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_STRIP_IN, INPUT_PULLUP);
  is_led_strip = digitalRead(LED_STRIP_IN) == HIGH;
  
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  if (is_led_strip) {
    strip.begin();
    initColors();
  } else {
    initButtons ();
    setupButtons ();
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
  //digitalWrite(ledPin2, HIGH);
  //Serial.println("led button color");

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

}


void scanButtons(){
  // TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  if(button1_pressed == 1)
    button1_pressed = 0;
  else
    button1_pressed = 1;


  if (button1_pressed)
      digitalWrite(ledPin, HIGH);
  else
      digitalWrite(ledPin, LOW);

  //Serial.print("button-");
  //Serial.print(button1_pressed);
  //Serial.println();
}


void pong () {
  String pong = "PONG !";

  connected = TRUE;

  if (connected) {
    Serial.println(pong);
    last_ping = millis();
  }

}
