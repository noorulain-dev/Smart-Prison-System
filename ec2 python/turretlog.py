from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import mysql.connector

mydb =  mysql.connector.connect(host="localhost", user="root", password="", database="iot")
mycursor = mydb.cursor()

ENDPOINT = "aita6dc6gzpsk-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "cloud_sub_turret_1"
PATH_TO_CERTIFICATE = "certs/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/AmazonRootCA1.pem"
TOPIC = "turret/act"

# Callback on message receive
def on_message_received(client, userdata, message):
   print(message.payload)
   json_data = json.loads(message.payload)
   act = json_data["act"]
   mycursor.execute("INSERT INTO turretLog (activity) VALUES (\"" + act+"\");")
   mydb.commit()
# Initialize MQTT client
mqtt_client = AWSIoTMQTTClient(CLIENT_ID)
mqtt_client.configureEndpoint(ENDPOINT, 8883)
mqtt_client.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)

# Connect and subscribe
mqtt_client.connect()
mqtt_client.subscribe(TOPIC, 0, on_message_received)

# Keep the script running
while True:
    pass
