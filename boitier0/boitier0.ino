#define boutonSwag 0
#define boutonN 1
#define boutonNE 2
#define boutonE 3
#define boutonSE 4
#define boutonS 5
#define boutonSO 6
#define boutonO 7
#define boutonNO 8
#define lumBoutonSwag 13
#define Red 11
#define Green 10
#define Blue 9

void setup() {
  // put your setup code here, to run once:
  int i;
  pinMode(lumBoutonSwag,OUTPUT);
  for (i=0; i<9 ; i++){
    pinMode(i,INPUT_PULLUP);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if (digitalRead(boutonSwag)){
    digitalWrite(lumBoutonSwag,LOW);
  } else {
    digitalWrite(lumBoutonSwag,HIGH);
  }
  
  delay(1);
  if (!digitalRead(boutonN)){
   writeColor(0,0,0);
  }
  
  if (!digitalRead(boutonNE)){
    writeColor(50,0,0);
  }
  
  if (!digitalRead(boutonE)){
    writeColor(50,50,0);
  }
  
  if (!digitalRead(boutonSE)){
    writeColor(0,50,0);
  }
  
  if (!digitalRead(boutonS)){
    writeColor(0,50,50);
  }
  
  if (!digitalRead(boutonSO)){
    writeColor(0,0,50);
  }

  if (!digitalRead(boutonO)){
    writeColor(50,0,50);
  }

  if (!digitalRead(boutonNO)){
    writeColor(50,50,50);
  }
  
  delay(50);
}

void writeColor(int r, int g, int b){
    analogWrite(Green,g);
    analogWrite(Blue,b);
    analogWrite(Red,r);
}
