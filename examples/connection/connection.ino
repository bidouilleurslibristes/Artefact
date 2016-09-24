
// 3 char ID
char * ARDUINO_ID = "L01";

#define TRUE 42
#define FALSE (!42)


// Functions definitions :
void connection ();


void setup() {
	Serial.begin(9600);
}

char connected = FALSE;

void loop () {
	connection();
	Serial.println("connected");
	delay (5000);
}


char back[3];
void connection () {
	connected = FALSE;

	// Connection
	while (!connected) {
		delay (1000);
		Serial.print("hello ");
		Serial.println(ARDUINO_ID);

		delay (10);

		if (Serial.available() >= 3) {
			back[0] = Serial.read();
			back[1] = Serial.read();
			back[2] = Serial.read();

			if (back[0] == ARDUINO_ID[0] && back[1] == ARDUINO_ID[1] && back[2] == ARDUINO_ID[2])
				connected = TRUE;
		}
	}
}