### Fuctions to Publish messages to AWS IoT Core
### Tested on Raspbian but should work on all linux based OS's
### AWS IoT SDK for Python v2 is needed install using the following command:
### pip install awsiotsdk

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import os #only needed if you are getting the hostname form OS

### Following variables need to be defined
# Define ENDPOINT, CLIENT_ID and TOPIC
CLIENT_ID = os.popen('hostname').readline().strip('\n') # This grabs the hostname but can be replaced witha string
ENDPOINT = "<PUT YOUR ENDPOINT HERE>"
# Paths to Amazon CA, Private cert and key
PATH_TO_CERT = "<PUT THE PATH TO YOUR CERT HERE>"
PATH_TO_KEY = "<PUT THE PATH TO YOUR KEY HERE>"
PATH_TO_ROOT = "<PUT THE PATH TO AMAZON CA HERE>"


### Fuction ###
def aws_publish_message(topic, message):
    ### Start of creating MQTT connection
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
                endpoint=ENDPOINT,
                cert_filepath=PATH_TO_CERT,
                pri_key_filepath=PATH_TO_KEY,
                client_bootstrap=client_bootstrap,
                ca_filepath=PATH_TO_ROOT,
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
    #print("Connected!")
    ### MQTT connection established
    mqtt_connection.publish(topic=topic, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + topic)
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    return()                          
### End of Fuctions


### Examples
aws_publish_message("test/function", {"ALERT" : "ALERT" })

message =  {"fuction-test" : "WORKING", "test" : 10 }
topic = "test/function"
aws_publish_message(topic, message)
