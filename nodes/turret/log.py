from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import mysql.connector

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
ENDPOINT = "aita6dc6gzpsk-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "HamzaRPI_sub_room_1"
ID2 = "tur_log"
PATH_TO_CERTIFICATE = "certs/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/AmazonRootCA1.pem"
TOPIC = "cell/turret"

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

mydb =  mysql.connector.connect(host="localhost", user="pi", password="password", database="turret")
mycursor = mydb.cursor()

def on_message_received(client, userdata, message):
    print(message.payload)
    json_data = json.loads(message.payload)
    cell = json_data["cell"]
    mycursor.execute("UPDATE cellTurn SET target = 1 WHERE cellNo = " + str(cell) + "")
    mydb.commit()
    
    
mqtt_client = AWSIoTMQTTClient(CLIENT_ID)
mqtt_client.configureEndpoint(ENDPOINT, 8883)
mqtt_client.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)

# Connect and subscribe
mqtt_client.connect()
mqtt_client.subscribe(TOPIC, 0, on_message_received)

while True:
    pass