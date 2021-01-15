### script that publishes devices stats to AWS
### Tested on Raspbian but should work on all linux based OS's
### AWS IoT SDK for Python v2 is needed install using the following command:
### pip install awsiotsdk

### Published message example ###
# {
#   "ramusage": 10.7,
#   "uptime": 8509,
#   "hostname": "R-Pi-Zero",
#   "cpuusage": 1.2,
#   "cputemp": 38.6
# }

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import os

### Defining Fuctions
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
### End of Fuctions

# Define ENDPOINT, CLIENT_ID and TOPIC
ENDPOINT = "a30knwf2xeu9vh-ats.iot.eu-west-2.amazonaws.com"
TOPIC = "test/device"
# Paths to Amazon CA, Private cert and key
PATH_TO_CERT = "/home/pi/aws-iot-core-raspberry-pi-demo/c4b1b5b8c9-certificate.pem.crt"
PATH_TO_KEY = "/home/pi/aws-iot-core-raspberry-pi-demo/c4b1b5b8c9-private.pem.key"
PATH_TO_ROOT = "/home/pi/aws-iot-core-raspberry-pi-demo/AmazonRootCA1.pem"
# How often to publish  status in seconds
SLEEPTIME = 10
# Gets hostname
CLIENT_ID = os.popen('hostname').readline().strip('\n')

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
print("Connected!")
### MQTT connection established

print('Begin Publish')
forever = "true"
while forever == "true":
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
    message = {"hostname" : CLIENT_ID, "uptime" : uptime, "cputemp" : CPUtemp, "cpuusage" : CPUusge, "ramusage" : RAMusage }
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'test/device'")
    t.sleep(SLEEPTIME)
print('Publish End')
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
