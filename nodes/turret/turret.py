from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
ENDPOINT = "aita6dc6gzpsk-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "HamzaRPI_pub_log_1"
ID2 = "tur_log"
PATH_TO_CERTIFICATE = "certs/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/AmazonRootCA1.pem"
TOPIC = "turret/act"

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


import cv2
import serial
import time
import mysql.connector

#setting up serial conenction to arduino
SerialObj = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
SerialObj.reset_input_buffer()
SerialObj.bytesize = 8   # Number of data bits = 8
SerialObj.parity  ='N'   # No parity
SerialObj.stopbits = 1   # Number of Stop bits = 1

#set up video capture
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FPS, 30)
vid.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
faceCascade = cv2.CascadeClassifier('/home/kiwimckiwiman/opencv-4.x/data/haarcascades/haarcascade_frontalface_alt.xml')
width = 320
height = 200

#variables
terminate = False;
timeLimit = 10;
#database credentials
mydb =  mysql.connector.connect(host="localhost", user="pi", password="password")
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS turret;")
mydb =  mysql.connector.connect(host="localhost", user="pi", password="password", database="turret")
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS settings(turretRange INT(3) NOT NULL PRIMARY KEY, turretActive TINYINT(1) NOT NULL);")
mycursor.execute("CREATE TABLE IF NOT EXISTS cellTurn(cellNo INT(1) NOT NULL PRIMARY KEY, target TINYINT(1) NOT NULL);")
mycursor.execute("SELECT * FROM settings")
result = mycursor.fetchone()
tRange = result[0]
tActive = result[1]
SerialObj.write(str(3).encode())
SerialObj.write((str(tRange) + "\n").encode())
SerialObj.write(str(tActive).encode())


mycursor.execute("SELECT * FROM cellTurn")
result = mycursor.fetchall()
def cam():
    start = time.time()
    while True:
        end = time.time()
        if(end - start > 25):
            cv2.destroyAllWindows()
            break;
        ret, frame = vid.read()
        frame = cv2.resize(frame, (320, 200))
        # Convert to greyscale for easier faster accurate face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist( gray )
        inst = 10
         # Do face detection to search for faces from these captures frames
        faces = faceCascade.detectMultiScale(frame, 1.1, 3, 0, (10, 10))
                  
        for (x, y, w, h) in faces:
             # Draw a green rectangle around the face (There is a lot of control to be had here, for example If you want a bigger border change 4 to 8)
             cv2.rectangle(frame, (x, y), (x + w,y +  h), (0, 255, 0), 4)
             x = x + (w/2)
             y = y + (h/2)
             
             break
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    

    
while True:
    mydb =  mysql.connector.connect(host="localhost", user="pi", password="password", database="turret")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM settings")
    result = mycursor.fetchone()
    if(result[0] != tRange or result[1] != tActive):
        print("changed")
        tRange = result[0]
        tActive = result[1]
        SerialObj.write(str(4).encode())
        SerialObj.write((str(tRange) + "\n").encode())
        SerialObj.write(str(tActive).encode())
        
    mydb =  mysql.connector.connect(host="localhost", user="pi", password="password", database="turret")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cellTurn")
    result = mycursor.fetchall()
    if(result[0][1] != 0):
        print(result[0][1])
        SerialObj.write(str(1).encode())
        mycursor.execute("UPDATE cellTurn SET target = 0 WHERE cellNo = 1")
        mydb.commit()
        cam()
    if(result[1][1] != 0):
        SerialObj.write(str(2).encode())
        mycursor.execute("UPDATE cellTurn SET target = 0 WHERE cellNo = 2")
        mydb.commit()
        cam()
        
    if SerialObj.in_waiting > 0: #if input from arduino
        detect = SerialObj.readline().decode('ascii').rstrip()
        if(detect == "shot"):
            data = {
                    "act": "shot"
                    }
            print("shot")
            mqtt_connection.publish(topic=TOPIC, payload=json.dumps(data), qos=mqtt.QoS.AT_MOST_ONCE)
        elif (detect == "det"):
            data = {
                    "act": "det"
                    }
            print("det")
            mqtt_connection.publish(topic=TOPIC, payload=json.dumps(data), qos=mqtt.QoS.AT_MOST_ONCE)
            