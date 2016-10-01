#define pinBouton 2

boolean etat;

void setup() {
   Serial.begin(9600);
   pinMode(pinBouton, INPUT);
}

void loop() {
   
  etat = digitalRead(pinBouton);

  if(etat == LOW) // appuyé
    Serial.write("1");


  delay(3000);
}
