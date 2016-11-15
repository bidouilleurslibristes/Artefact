int cols[] = {8, 9, 10};
int rows[] = {11, 12, 13};

void setup() {
  // Setup button entries
  for(int i=0 ; i<3 ; i++) {
    pinMode(cols[i], INPUT_PULLUP);
    pinMode(rows[i], OUTPUT);
    digitalWrite(rows[i], LOW);
  }
  Serial.begin(9600);

  // Main loop
  while (42) {
    delay(10);
    main_loop();
  }
}

void main_loop () {
  String buttons = "";

  for (int row=0 ; row<3 ; row++) {
    digitalWrite(rows[row], HIGH);
    for (int col=0 ; col<3 ; col++) {
      int val = digitalRead(cols[col]) == LOW;
      buttons += (char)('0' + val);
    }
    digitalWrite(rows[row], LOW);
  }

  Serial.println(buttons);
}

void loop() {}
