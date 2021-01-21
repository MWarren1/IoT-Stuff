### waiting on button press to Publish messages to AWS IoT Core
### should work on all 40 pin raspberry Pi's

### AWS IoT SDK for Python v2 and gpiozero is needed install using the following commands:
### sudo pip install awsiotsdk
### sudo apt install python3-gpiozero

### other Setup
### hardware:
### connect one side of the button up to a ground pin (Pin 6)and the other to GPIO4 (Pin 7) 

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import os #only needed if you are getting the hostname form OS
from gpiozero import Button
import awsconfig #import config needed for aws

### Following defined by awsconfig.py file ###
# AWS Endpoint
ENDPOINT = awsconfig.ENDPOINT
# Gets hostname
CLIENT_ID = awsconfig.CLIENT_ID
# Paths to Amazon CA, Private cert and key
PATH_TO_CERT = awsconfig.PATH_TO_CERT
PATH_TO_KEY = awsconfig.PATH_TO_KEY
PATH_TO_ROOT = awsconfig.PATH_TO_ROOT
### End of awsconfig.py variables ###


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
### End of Fuction ###
### Start of Code ###
button = Button(4)
forever = "true"

while forever == "true":

    print("\nWaiting for button press:\n")
    button.wait_for_press()
    aws_publish_message("test/alert", {"ALERT" : "ALERT" , "Client" : CLIENT_ID })

