const int SPEAKER_BUTTON_PIN = 2;
const int LED_BUTTON_PIN = 3;
const int LED_PIN = 4;
const int SPEAKER_PIN = 5;

bool speakerOn = false;
bool ledOn = false;
String received_command;

void setup() {
  pinMode(SPEAKER_PIN, OUTPUT);  
  pinMode(SPEAKER_BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (digitalRead(SPEAKER_BUTTON_PIN) == LOW) {
      digitalWrite(SPEAKER_PIN, !speakerOn); // Toggle the speaker state
      speakerOn = !speakerOn;
      delay(500); // Debounce delay
    }
  
  // Check if the LED button is pressed
  if (digitalRead(LED_BUTTON_PIN) == LOW) {
    digitalWrite(LED_PIN, !ledOn); // Toggle the LED state
    ledOn = !ledOn;
    delay(500); // Debounce delay  
  }
  if (Serial.available() > 0) {
    received_command = Serial.readStringUntil("\n");    
    received_command.trim();
    if (received_command == "browser") {
      analogWrite(LED_PIN, 204);
      ledOn = true;
      delay(500);
    }
    else if (received_command == "light on") {
      digitalWrite(LED_PIN, HIGH);        
      ledOn = true;
      delay(500);
    }
    else if (received_command == "speaker on") {
      if (!speakerOn) {
        digitalWrite(SPEAKER_PIN, HIGH);        
        delay(2500);
        speakerOn = true;
      }
    }
     else if (received_command == "light off") {
      digitalWrite(LED_PIN, LOW);        
      ledOn = false;
      delay(500);
    }
    else if (received_command == "speaker off") {
      if (speakerOn) {
        digitalWrite(SPEAKER_PIN, LOW);        
        delay(2500);
        speakerOn = false;
      }
    }
    else if (received_command == "audio") {
      analogWrite(LED_PIN, 204);
      ledOn = true;      
      delay(500);
      if (!speakerOn) {
        digitalWrite(SPEAKER_PIN, HIGH);        
        delay(3000);
        speakerOn = true;
      }
    }
    else if (received_command == "video") {
      analogWrite(LED_PIN, LOW);
      ledOn = false;
      if (!speakerOn) {
        digitalWrite(SPEAKER_PIN, HIGH);        
        delay(2500);
        speakerOn = true;
      }
    } 
    else if (received_command == "document") {
      digitalWrite(SPEAKER_PIN, LOW);
      speakerOn = false;
      digitalWrite(LED_PIN, HIGH);        
      ledOn = true;
      delay(500);
    }
    else if (received_command == "code") {
      digitalWrite(LED_PIN, HIGH);        
      ledOn = true;
      delay(500);
      if (!speakerOn) {
        digitalWrite(SPEAKER_PIN, HIGH);        
        delay(2500);
        speakerOn = true;
      }
    }
    else if (received_command == "sleep") {
      digitalWrite(SPEAKER_PIN, LOW);
      speakerOn = false;
      digitalWrite(LED_PIN, LOW);
      ledOn = false;
      delay(500);
    }    
  }
}
