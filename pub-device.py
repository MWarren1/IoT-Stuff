### script that publishes devices stats to AWS
### Tested on Raspbian but should work on all linux based OS's

### Published message example ###
# {
#   "uptime": 15289,
#   "hostname": "R-Pi-Zero",
#   "cpuusage": 2.6,
#   "time": "14:30:13",
#   "cputemp": 36.5,
#   "date": "2021/01/19",
#   "ramusage": 10.8
# }

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import os
import awsconfig

# Define Topic to publish message to
TOPIC = "test/device"
# How often to publish  status in seconds
SLEEPTIME = 10

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

### Defining Fuctions ###
# Return CPU temperature as a character string, temp in 'C                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

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
### End of Fuctions ###


forever = "true"
while forever == "true":
    # Get current time/date
    time_raw = t.localtime()
    current_time = t.strftime("%H:%M:%S", time_raw)
    current_date = t.strftime("%Y/%m/%d", time_raw)
    # Generate key
    key = CLIENT_ID + "-" + str(t.time())
    # Get Uptime
    uptime_raw = os.popen("awk '{print $1}' /proc/uptime").readline()
    uptime = int(float(uptime_raw.strip('\n')))
    # Get CPU Temperature in 'C
    CPUtemp = round(float(getCPUtemperature()),1)
    # Get CPU Usage in %
    CPUusge = round(float(getCPUuse()),1)
    # Get RAM Usage in %
    RAMstats = getRAMinfo()
    RAMusage = round((float(RAMstats[1])/float(RAMstats[0]))*100,1)
    
    # create message and publish
    message = {"key" : key, "date" : current_date, "time" : current_time, "hostname" : CLIENT_ID, "uptime" : uptime, "cputemp" : CPUtemp, "cpuusage" : CPUusge, "ramusage" : RAMusage }
    aws_publish_message(TOPIC, message)
    t.sleep(SLEEPTIME)
