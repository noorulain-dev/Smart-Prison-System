#mqtt
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

ENDPOINT = "aita6dc6gzpsk-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "NoorRPI_pub_env_1"
PATH_TO_CERTIFICATE = "certs/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/AmazonRootCA1.pem"
TOPIC = "cell/env"
RANGE = 1

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
mydb =  mysql.connector.connect(host="localhost", user="pi", password="password", database="cell")
mycursor = mydb.cursor()

import time
start = time.time()
while True:
    end = time.time()
    if((end - start) > 10):
        start = time.time()
        mycursor.execute("SELECT AVG(temp) AS avg_temp, AVG(humid) AS avg_humid, AVG(noise) AS avg_noise FROM env;")
        result = mycursor.fetchone()
        data = {
                 "cell": "1",
                 "temp": str(f"{result[0]:.2f}"),
                 "humid": str(f"{result[1]:.2f}"),
                 "noise": str(f"{result[2]:.2f}")
             }
        mqtt_connection.publish(topic=TOPIC, payload=json.dumps(data), qos=mqtt.QoS.AT_MOST_ONCE)
        mycursor.execute("DELETE FROM env;")
        mydb.commit()

disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()