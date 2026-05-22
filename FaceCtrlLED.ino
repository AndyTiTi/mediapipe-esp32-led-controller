int ledPin = 18;  // 确认你的LED接在Pin 18
bool ledState = false;
String inputBuffer = "";

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  digitalWrite(ledPin, LOW);
  delay(1000);
  Serial.println("=== Arduino LED Control Ready ===");
  Serial.print("LED Pin: ");
  Serial.println(ledPin);
  
  // 测试LED闪烁3次
  for (int i = 0; i < 3; i++) {
    digitalWrite(ledPin, HIGH);
    delay(200);
    digitalWrite(ledPin, LOW);
    delay(200);
  }
  Serial.println("LED test complete. Waiting for commands...");
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    
    if (c == '\n' || c == '\r') {
      if (inputBuffer.length() > 0) {
        Serial.print("Received: [");
        Serial.print(inputBuffer);
        Serial.println("]");
        
        if (inputBuffer == "ON") {
          ledState = true;
          digitalWrite(ledPin, HIGH);
          Serial.println("-> LED ON (Pin 18 HIGH)");
        } 
        else if (inputBuffer == "OFF") {
          ledState = false;
          digitalWrite(ledPin, LOW);
          Serial.println("-> LED OFF (Pin 18 LOW)");
        }
        else {
          Serial.println("-> Unknown command");
        }
        inputBuffer = "";
      }
    } 
    else {
      inputBuffer += c;
    }
  }
}
