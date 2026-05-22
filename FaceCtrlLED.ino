/*
 * Hand Control Dual LED System
 * Left Hand  -> LED1 (Pin 18)
 * Right Hand -> LED2 (Pin 17)
 */

int led1Pin = 18;  // 左手控制
int led2Pin = 17;  // 右手控制
String inputBuffer = "";

void setup() {
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  Serial.begin(9600);
  
  digitalWrite(led1Pin, LOW);
  digitalWrite(led2Pin, LOW);
  
  delay(1000);
  Serial.println("========================================");
  Serial.println("   Dual LED Control System Ready");
  Serial.println("========================================");
  Serial.println("LED1 (Pin 18) - Left Hand");
  Serial.println("LED2 (Pin 17) - Right Hand");
  Serial.println("========================================");
  
  // LED 测试：交替闪烁 3 次
  for (int i = 0; i < 3; i++) {
    digitalWrite(led1Pin, HIGH);
    delay(150);
    digitalWrite(led1Pin, LOW);
    digitalWrite(led2Pin, HIGH);
    delay(150);
    digitalWrite(led2Pin, LOW);
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
        
        // 左手控制 LED1 (Pin 18)
        if (inputBuffer == "LON") {
          digitalWrite(led1Pin, HIGH);
          Serial.println("-> LED1 (Pin 18) ON");
        } 
        else if (inputBuffer == "LOFF") {
          digitalWrite(led1Pin, LOW);
          Serial.println("-> LED1 (Pin 18) OFF");
        }
        // 右手控制 LED2 (Pin 17)
        else if (inputBuffer == "RON") {
          digitalWrite(led2Pin, HIGH);
          Serial.println("-> LED2 (Pin 17) ON");
        }
        else if (inputBuffer == "ROFF") {
          digitalWrite(led2Pin, LOW);
          Serial.println("-> LED2 (Pin 17) OFF");
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
