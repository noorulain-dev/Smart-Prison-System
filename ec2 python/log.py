from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import mysql.connector

mydb =  mysql.connector.connect(host="localhost", user="root", password="", database="iot")
mycursor = mydb.cursor()

ENDPOINT = "aita6dc6gzpsk-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "cloud_sub_1"
PATH_TO_CERTIFICATE = "certs/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/AmazonRootCA1.pem"
TOPIC = "cell/log"

# Callback on message receive
def on_message_received(client, userdata, message):
    print(message.payload)
    json_data = json.loads(message.payload)
    tag = json_data["tag"]
    cell = json_data["cell"]
    activity = json_data["activity"]

    mycursor.execute("INSERT INTO patrol (cellID, guardID, activityName) VALUES ("+cell+",\""+tag+"\",\""+activity+"\");")
    mydb.commit()
# Initialize MQTT client
mqtt_client = AWSIoTMQTTClient(CLIENT_ID)
mqtt_client.configureEndpoint(ENDPOINT, 8883)
mqtt_client.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)

# Connect and subscribe
mqtt_client.connect()
mqtt_client.subscribe(TOPIC, 0, on_message_received)
print(f"Subscribed to topic: {TOPIC}")

# Keep the script running
while True:
    pass
