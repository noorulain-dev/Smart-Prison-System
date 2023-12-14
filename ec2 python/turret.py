from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import mysql.connector

mydb =  mysql.connector.connect(host="localhost", user="root", password="", database="iot")
mycursor = mydb.cursor()

ENDPOINT = "aita6dc6gzpsk-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "cloud_sub_settings_1"
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

connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

cell = 0
while True:
    mydb =  mysql.connector.connect(host="localhost", user="root", password="", database="iot")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM env WHERE temp > 25 AND envTime >= NOW() - INTERVAL 30 SECOND ORDER BY temp DESC LIMIT 1")
    result = mycursor.fetchone()
    
    if result is not None:
        if (cell != result[1]):
            cell = result[1]
            print(cell)
            message = {"cell" : str(result[1])}
            mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_MOST_ONCE)
            mycursor.execute("UPDATE cell SET buzz = 1 WHERE cellID = " + str(cell))
            mydb.commit()
    t.sleep(1)

disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
