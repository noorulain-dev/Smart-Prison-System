from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

ENDPOINT = "aita6dc6gzpsk-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "NoorRPI_sub_settings_1"
PATH_TO_CERTIFICATE = "certs/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/AmazonRootCA1.pem"
TOPIC = "cell/settings"

import mysql.connector
mydb =  mysql.connector.connect(host="localhost", user="pi", password="password", database="cell")
mycursor = mydb.cursor()

# Callback on message receive
def on_message_received(client, userdata, message):
    print(message.payload)
    json_data = json.loads(message.payload)
    buzz = json_data["buzz"]
    door = json_data["door"]
    
    mycursor.execute("UPDATE settings SET settingsVal = " + str(buzz) + " WHERE settingsType = \"buzzer\"")
    mycursor.execute("UPDATE settings SET settingsVal = " + str(door) + " WHERE settingsType = \"door\"")
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