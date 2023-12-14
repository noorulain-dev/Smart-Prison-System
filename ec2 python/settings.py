from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import mysql.connector

mydb =  mysql.connector.connect(host="localhost", user="root", password="", database="iot")
mycursor = mydb.cursor()

ENDPOINT = "aita6dc6gzpsk-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "cloud_sub_settings_8"
PATH_TO_CERTIFICATE = "certs/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/AmazonRootCA1.pem"
TOPIC = "cell/settings"

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

doorVal = 0
buzzerVal = 0

while True:
    mydb =  mysql.connector.connect(host="localhost", user="root", password="", database="iot")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT buzz, openDoor FROM cell WHERE cellID = 1")
    result = mycursor.fetchone()
    #print(result)
    if(buzzerVal != result[0]):
        print(result)
        message = {"buzz" : str(result[0]), "door" : str(result[1])}
        mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_MOST_ONCE)
        mycursor.execute("UPDATE cell SET buzz = 0 WHERE cellID = 1")
        mydb.commit()

    if(doorVal != result[1]):
        print(result)
        message = {"buzz" : str(result[0]), "door" : str(result[1])}
        mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_MOST_ONCE)
        doorVal = result[1]
    t.sleep(1)

disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
