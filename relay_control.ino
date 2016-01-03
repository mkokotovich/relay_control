#define DEBUG 1

#define RELAY_PIN 12
#define DEBUG_PIN 13

void setup() {
  // put your setup code here, to run once:
  
  // Optional debug pin, just to show a light
  // when we have power to the relay
  if (DEBUG)
  {
    // initialize digital pin 13 as an output
    pinMode(DEBUG_PIN, OUTPUT);
  }

  // initialize relay pin as an output
  pinMode(RELAY_PIN, OUTPUT);

  // start serial port at 9600 bps:
  Serial.begin(9600);
  while (!Serial)
  {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  // put your main code here, to run repeatedly:

  int inByte = 0;         // incoming serial byte

  // Read data off serial
  if (Serial.available() > 0)
  {
    // get incoming byte:
    inByte = Serial.read();
    if (inByte == '0')
    {
      send_signal(LOW);
    }
    else if (inByte == '1')
    {
      send_signal(HIGH);
    }
  }
}

void send_signal(int voltage)
{
  if (DEBUG)
  {
    digitalWrite(DEBUG_PIN, voltage); 
  }
  digitalWrite(RELAY_PIN, voltage); 
}

