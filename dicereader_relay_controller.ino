// This is the sketch for the Arduino
// Relay pin is controlled with D8. The active wire is connected to Normally Closed and common
int relay = 8;
volatile byte relayState = LOW;

void setup() {
  pinMode(relay, OUTPUT);
  Serial.begin( 9600 );
}

void loop() {
  if (Serial.available()>0) {
    if (Serial.read() == '1') {
      digitalWrite(relay, HIGH);
      delay(200);
    } else
    {
      digitalWrite(relay, LOW);
    }
  }
  digitalWrite(relay, LOW);
}