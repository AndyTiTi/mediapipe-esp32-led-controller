/*
 * Hand Control Dual LED System
 * Left Hand  -> LED1 (Pin 8)
 * Right Hand -> LED2 (Pin 18)
 * 
 * 串口说明:
 * - Serial (USB) -> 与 Python 通信
 * - Serial2 (Pin 17=TX) -> 调试日志输出
 */

int led1Pin = 8;   // 左手控制
int led2Pin = 18;  // 右手控制
String inputBuffer = "";

// 调试日志宏
#define DEBUG_LOG(msg) Serial2.println(msg)

void setup() {
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  
  Serial.begin(9600);
  
  // Serial2: 显式指定引脚 (RX=16, TX=17)
  Serial2.begin(115200, SERIAL_8N1, 16, 17);
  
  digitalWrite(led1Pin, LOW);
  digitalWrite(led2Pin, LOW);
  
  delay(1000);
  
  DEBUG_LOG("========================================");
  DEBUG_LOG("   Dual LED Control System Ready");
  DEBUG_LOG("========================================");
  DEBUG_LOG("LED1 - Left Hand");
  DEBUG_LOG("LED2 - Right Hand");
  DEBUG_LOG("Debug Serial2: Pin 17 (TX) @ 115200 baud");
  DEBUG_LOG("========================================");
  
  // LED 测试
  for (int i = 0; i < 3; i++) {
    digitalWrite(led1Pin, HIGH);
    delay(150);
    digitalWrite(led1Pin, LOW);
    digitalWrite(led2Pin, HIGH);
    delay(150);
    digitalWrite(led2Pin, LOW);
  }
  DEBUG_LOG("LED test complete. Waiting for commands...");
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    
    if (c == '\n' || c == '\r') {
      if (inputBuffer.length() > 0) {
        DEBUG_LOG("----------------------------------------");
        DEBUG_LOG("Received: [" + inputBuffer + "]");
        
        if (inputBuffer == "LON") {
          digitalWrite(led1Pin, HIGH);
          DEBUG_LOG("Action: LED1 ON");
        } 
        else if (inputBuffer == "LOFF") {
          digitalWrite(led1Pin, LOW);
          DEBUG_LOG("Action: LED1 OFF");
        }
        else if (inputBuffer == "RON") {
          digitalWrite(led2Pin, HIGH);
          DEBUG_LOG("Action: LED2 ON");
        }
        else if (inputBuffer == "ROFF") {
          digitalWrite(led2Pin, LOW);
          DEBUG_LOG("Action: LED2 OFF");
        }
        else {
          DEBUG_LOG("Action: Unknown command");
        }
        inputBuffer = "";
      }
    } 
    else {
      inputBuffer += c;
    }
  }
}
