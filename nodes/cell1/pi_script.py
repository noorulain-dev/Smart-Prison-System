#mqtt
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

ENDPOINT = "aita6dc6gzpsk-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "NoorRPI_pub_log_1"
PATH_TO_CERTIFICATE = "certs/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/AmazonRootCA1.pem"
TOPICACT = "cell/log"

event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")

#mysql
import mysql.connector
mydb =  mysql.connector.connect(host="localhost", user="pi", password="password")
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS cell;")
mydb =  mysql.connector.connect(host="localhost", user="pi", password="password", database="cell")
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS env(id int(11) AUTO_INCREMENT PRIMARY KEY, temp DECIMAL(4,2) NOT NULL, humid DECIMAL(4,2) NOT NULL, noise int(4) NOT NULL, timeRec TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);")

#serial
import serial
SerialObj = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
SerialObj.reset_input_buffer()
SerialObj.bytesize = 8   # Number of data bits = 8
SerialObj.parity  ='N'   # No parity
SerialObj.stopbits = 1   # Number of Stop bits = 1

#vars
tags = ["C37E7E1A","B34FA618"]

#webcam setup
import cv2
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FPS, 30)
vid.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
width = 320
height = 200

#facial recog setup
import dlib
import glob
import numpy as np
import os
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

def auth(dir):
  dets = detector(dir, 1)
  lowest = ("no", 0)
  if(len(dets) == 0):
      return "no"
  else:
      for k, d in enumerate(dets):
        shape = sp(dir, d)
        face_descriptor = facerec.compute_face_descriptor(dir, shape)
        auth = np.array(face_descriptor)
      for filename in os.listdir("embeddings"):
        emb = np.load(os.path.join("embeddings", filename))
        score = np.dot(auth,emb)/(np.linalg.norm(auth)*np.linalg.norm(emb))
        if(score > lowest[1] and score > 0.97):
          lowest = (filename.split(".")[0], score)
      return (lowest[0])
    
def facerecog():
    j = 0
    while j < 5:
        j = j + 1
        ret, frame = vid.read()
        frame = cv2.resize(frame, (320, 200))
        res = auth(frame)
        if (res != "no"):
            return 1
    return 0

def check(doorClosed):
    for x in tags:
        if x == getTag:
            if (doorClosed == True):
                found = facerecog()
                if (found == 0):
                    print(getTag + "|cell 1|visited")
                    data = {
                            "tag": getTag,
                            "cell": "1",
                            "activity": "visited"
                            }
                    mqtt_connection.publish(topic=TOPICACT, payload=json.dumps(data), qos=mqtt.QoS.AT_MOST_ONCE)
                else:
                    print(getTag + "|cell 1|opened")
                    data = {
                            "tag": getTag,
                            "cell": "1",
                            "activity": "opened"
                            }
                    mqtt_connection.publish(topic=TOPICACT, payload=json.dumps(data), qos=mqtt.QoS.AT_MOST_ONCE)
                    
                    
                    mycursor.execute("UPDATE settings SET settingsVal = 1 WHERE settingsType = \"door\";")
                    
                    
                return found
            else:
                print(getTag + "|cell 1|closed")
                data = {
                            "tag": getTag,
                            "cell": "1",
                            "activity": "closed"
                            }
                mqtt_connection.publish(topic=TOPICACT, payload=json.dumps(data), qos=mqtt.QoS.AT_MOST_ONCE)
                
                mycursor.execute("UPDATE settings SET settingsVal = 0 WHERE settingsType = \"door\";")
                
                return 1
    return 0

#main loop
closed = True
loop = 0

buzzerVal = 0
doorVal = 0

while True:
    mycursor.execute("SELECT settingsVal FROM settings WHERE settingsType = \"buzzer\";")
    result = mycursor.fetchone()
    if (buzzerVal != result[0]):
        SerialObj.write(str(2).encode())
        mycursor.execute("UPDATE settings SET settingsVal = 0 WHERE settingsType = \"buzzer\";")
        
    mycursor.execute("SELECT settingsVal FROM settings WHERE settingsType = \"door\";")
    result = mycursor.fetchone()
    if (doorVal != result[0]):
        SerialObj.write(str(3).encode())
        doorVal = result[0]
        if(closed == True):
            closed = False
        else:
            closed = True
            
    if SerialObj.in_waiting > 0: #if input from arduino
        rec = SerialObj.readline().decode('ascii').rstrip()
        if (rec == "tag"):
            getTag = SerialObj.readline().decode('ascii').rstrip()
            found = check(closed)
            SerialObj.write(str(found).encode())
            if(found == 1):
                if(closed == True):
                    closed = False
                    doorVal = 1
                else:
                    closed = True
                    doorVal = 0
        else:
            if (loop == 10):
                print(rec)
                temp, humid, noise = rec.split("|")
                query = "INSERT into env (temp, humid, noise) VALUES ("+str(temp)+", "+str(humid)+","+str(noise)+");"
                mycursor.execute(query)
                mydb.commit()
                loop = 0
            else:
                loop = loop + 1