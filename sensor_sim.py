### Sensor simulator
### publishes dataset with delay as to simulate a IoT sensor

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import json
import os #only needed if you are getting the hostname form OS
import awsconfig #import config needed for aws
import csv
import argparse
import os.path
import time
import sys

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
    #print("Connecting to {} with client ID '{}'...".format(ENDPOINT, CLIENT_ID))
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


## CLI switches
parser = argparse.ArgumentParser(prog='sensor simulator', description='simulates a IoT sensor by publishing messages from a data set in a csv file')
parser.add_argument('--dataset', required=True, help='file input(must be csv)')
parser.add_argument('--delay', required=True, help='time in seconds between published messages')
parser.add_argument('--topic', required=True, help='topic that messages will get published to')

args = parser.parse_args()
## End of CLI switches

# delay between published messages
delay = int(args.delay)
# topic that messages will get published to
topic = args.topic
# open dataset
with open(args.dataset, 'Ur') as f:
    
    line_count = 0
    parserreader = csv.reader(f)
    for row in parserreader:
        if line_count == 0:
            # collect column names
            print("Following fields will be published:")
            print(', '.join(row))
            column_total = len(row)
            column = 0
            column_list = []
            while column < column_total:
                column_list.append(row[column])
                column = column + 1
            line_count = line_count + 1
        else:
            # creating the message
            column = 0
            message = {}
            while column < column_total:
                message[column_list[column]] = row[column]
                column = column + 1
            # Publish message
            aws_publish_message(topic, message)
            time.sleep(delay)
