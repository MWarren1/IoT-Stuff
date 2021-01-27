##### Script to measure distance and publish messages 
##### How to use:
##### place sensor pointing at a hard object like a wall and run script,
##### while the status LED is flashing(around 5 secs) the sensor is taking the baseline distance.
##### when the status LED is solid the script is now monitoring distance and 
##### while the distance is 75% or less of the baseline and message will published to AWS IoT Core

########### Circuit Diagram #############
#
# +5v------------------------------------
#                                |
#                               Vcc						 
#                          --------------
# GPIO18---------------Trig| Ultrasonic |
# GPIO24---R1----------Echo|   Sensor   |
#                   |      --------------
#                   |           Gnd
# GPIO26--R1-----   |            |
# GPIO19--R1-   |   R2           |
#           |   |   |            |
#          LED LED  |            | 
#           |   |   |            |
# Gnd------------------------------------
# 
# R1 = 330 ohm
# R2 = 470 ohm
# Ultrasonic Sensor = HC-SR04 Module
#
#########################################

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import json
import os #only needed if you are getting the hostname form OS
import awsconfig #import config needed for aws
import RPi.GPIO as GPIO
import time

##### User Defined Variabled #####
TOPIC = "test/desk_monitor" # topic that messages will get published to
SLEEPTIME = 1 # how often in seconds distance will be checked
##### End of User Defined Variabled #####

##### Setting Up GPIO's #####
### set GPIO Pins - These can be changed to what is used 
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_LED_ALERT = 19
GPIO_LED_STATUS = 26

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_LED_ALERT, GPIO.OUT)
GPIO.setup(GPIO_LED_STATUS, GPIO.OUT)
# set LED's to low
GPIO.output(GPIO_LED_ALERT, False)
GPIO.output(GPIO_LED_STATUS, False)

##### Following defined by awsconfig.py file #####
# AWS Endpoint
ENDPOINT = awsconfig.ENDPOINT
# Gets hostname
CLIENT_ID = awsconfig.CLIENT_ID
# Paths to Amazon CA, Private cert and key
PATH_TO_CERT = awsconfig.PATH_TO_CERT
PATH_TO_KEY = awsconfig.PATH_TO_KEY
PATH_TO_ROOT = awsconfig.PATH_TO_ROOT
##### End of awsconfig.py variables #####

##### Start of Fuctions #####
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

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

##### End of Fuctions #####

##### Start of Script ##### 
if __name__ == '__main__':
    ### get baseline distance
    n = 1
    dist_list = []
    print (" Getting Distance Baseline:")
    while n <=25:
        if GPIO.input(GPIO_LED_STATUS) == 1:
            # set LED to low
            GPIO.output(GPIO_LED_STATUS, False)
        else:
            # set LED to high
            GPIO.output(GPIO_LED_STATUS, True)              
        dist_list.append(int(distance()))
        time.sleep(0.2)
        n = n+1
    baseline = sum(dist_list) / len(dist_list)
    del dist_list[:]
    print("Distance Baseline: " + str(baseline) + "cm")    
    # set status LED to high
    if GPIO.input(GPIO_LED_STATUS) == 0:
        # set LED to low
        GPIO.output(GPIO_LED_STATUS, True)
    
    ### Starting Monitoring
    try:
        lastdist = 0
        while True:
            dist = distance() # distance in cm
            # checks if distance is less than or equal to 75% of baseline 
            if int(dist) <= (baseline/4)*3:
                # set LED to High
                GPIO.output(GPIO_LED_ALERT, True)
                aws_publish_message(TOPIC, { "CLIENT_ID": CLIENT_ID, "distance" : int(dist), "baseline" : baseline })
                print ("ALERT - Measured Distance = " + str(int(dist)) + "cm    Baseline = " + str(baseline) + "cm")
            else:
                # set LED to low
                GPIO.output(GPIO_LED_ALERT, False)
                print ("Measured Distance = " + str(int(dist)) + "cm    Baseline = " + str(baseline) + "cm")                
            
            time.sleep(SLEEPTIME)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        
