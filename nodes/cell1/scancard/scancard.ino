#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include "DHT.h"

#define RST_PIN 9
#define SS_PIN 10
#define DHT11_PIN 6
#define Noise A0

DHT dht11(DHT11_PIN, DHT11);
Servo servo;

byte readCard[4];
String tagID = "";
int buzzer = 7;
int angle = 0;

// Create instances
MFRC522 mfrc522(SS_PIN, RST_PIN);


boolean getID(){ 
  if ( ! mfrc522.PICC_IsNewCardPresent()) { //If a new PICC placed to RFID reader continue
  return false;
  }
  if ( ! mfrc522.PICC_ReadCardSerial()) { //Since a PICC placed get Serial and continue
  return false;
  }
  tagID = "";
  for ( uint8_t i = 0; i < 4; i++) { // The MIFARE PICCs that we use have 4 byte UID
  tagID.concat(String(mfrc522.uid.uidByte[i], HEX)); // Adds the 4 bytes in a single String variable
  }
  tagID.toUpperCase();
  mfrc522.PICC_HaltA(); // Stop reading
  return true;
}

void buzz(int del){
  for(int i=0;i<80;i++){
    digitalWrite(buzzer,HIGH);
    delay(del);//wait for 1ms
    digitalWrite(buzzer,LOW);
    delay(del);//wait for 1ms
  }
}

void setup() 
{
  // Initiating
  Serial.begin(9600);
  SPI.begin(); // SPI bus
  dht11.begin();
  mfrc522.PCD_Init(); // MFRC522
  servo.attach(8);
  servo.write(0);
  pinMode(buzzer,OUTPUT);
  pinMode(Noise, INPUT);
}

void loop(){
  float humi  = dht11.readHumidity();
  float tempC = dht11.readTemperature();
  int dcb = analogRead(Noise);
  String env = String(tempC) + "|" + String(humi) + "|" + String(dcb);
  Serial.println(env); // Send the data

  delay(500);
  if(Serial.available()>0){
    int action = Serial.read();
    if(action == 50){
      buzz(3);
    }else if(action == 51){
      if(angle < 180){
        for(angle = 0; angle < 180; angle++){                                  
          servo.write(angle);               
          delay(5);                   
        }
      }else{
        for(angle = 180; angle > 0; angle--){                                
          servo.write(angle);           
          delay(5);       
       } 
      }
    }
  }
  while (getID()){
      Serial.println("tag");
      delay(100);
      Serial.println(tagID);
      delay(3000);
      if(Serial.available()>0){
         int found = Serial.read();
         delay(100);
         //Serial.println(found);
         delay(100);
         if(found == 49){
           buzz(1);
           if(angle < 180){
             for(angle = 0; angle < 180; angle++){                                  
               servo.write(angle);               
               delay(5);                   
             }
           }else{
             for(angle = 180; angle > 0; angle--){                                
               servo.write(angle);           
               delay(5);       
             } 
           }
         }else if(found == 48){
            buzz(2);
         }
      } 
   }
}
  
