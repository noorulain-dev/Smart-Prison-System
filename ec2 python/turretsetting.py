from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import mysql.connector

mydb =  mysql.connector.connect(host="localhost", user="root", password="", database="iot")
mycursor = mydb.cursor()

ENDPOINT = "aita6dc6gzpsk-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "cloud_sub_settings_12"
PATH_TO_CERTIFICATE = "certs/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/AmazonRootCA1.pem"
TOPIC = "cell/turretsettings"

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

connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

tRange = 30
tActive = 1

while True:
    mydb =  mysql.connector.connect(host="localhost", user="root", password="", database="iot")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM turret;")
    result = mycursor.fetchone()
    #print(result)
    if(tRange != result[0]):
        print(result)
        message = {"range" : str(result[0]), "active" : str(result[1])}
        mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_MOST_ONCE)
        tRange = result[1]

    if(tActive != result[1]):
        print(result)
        message = {"range" : str(result[0]), "active" : str(result[1])}
        mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_MOST_ONCE)
        tActive = result[1]
    t.sleep(1)

disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
