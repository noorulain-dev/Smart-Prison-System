int trigPin = 2;
int echoPin = 3;
bool active = false;
int limit = 10;
void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT);
  pinMode(A2, OUTPUT);
  
}

void loop() {
  
  if(Serial.available() > 0){
    bool getLim = false;
    bool getActive = false;
    int input = Serial.read();
    
    if(input == 51){
      delay(100);
      if (Serial.available()>0 && getLim == false){
          String in = Serial.readStringUntil('\n');
          limit = in.toInt();
          getLim = true;
          digitalWrite(A3, HIGH);
          String act = Serial.readString();
          getActive = true;
          if(act == "1"){
            active = true;
            digitalWrite(A5, HIGH);
          }else if(act == "0"){
            active = false;
            digitalWrite(A5, LOW);
          }
       }
    }else if(input == 52){
      delay(100);
      if (Serial.available()>0 && getLim == false){
          String in = Serial.readStringUntil('\n');
          limit = in.toInt();
          digitalWrite(A4, HIGH);
          String act = Serial.readString();
          if(act == "1"){
            active = true;
            digitalWrite(A5, HIGH);
          }else if(act == "0"){
            active = false;
            digitalWrite(A5, LOW);
          }
          delay(500);
          digitalWrite(A4, LOW);
       }
    }else if(input == 49){
      digitalWrite(A0, HIGH);
      delay(5000);
      digitalWrite(A0, LOW);
    }else if(input == 50){
      digitalWrite(A1, HIGH);
      delay(5000);
      digitalWrite(A1, LOW);
    }
  }
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    int duration = pulseIn(echoPin, HIGH);
    int distance = duration * 0.034 / 2;
    //Serial.println(distance);
    delay(100);
    if(distance < limit){
      if(active){
        Serial.println("shot");
        digitalWrite(A2, HIGH);
      }else if (active == false){
        Serial.println("det");
      }
    }else{
      digitalWrite(A2, LOW);
    }

}
