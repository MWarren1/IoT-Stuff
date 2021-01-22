# IoT-Stuff
dumping ground for IoT stuff

## Requirments/Setup
the following packages/modules are needed for all these scripts:
* sudo apt-get install cmake
* sudo apt-get install libssl-dev
* pip install awsiotsdk

also the all your aws variables need to be added to awsconfig.py

## Scripts

### Pub_Device.py
publishes stats about the deivce to AWS until stopped

### Pub_Function.py
Function for publishing messages to topics. 

### Pub_Button.py
shows basic use of Raspberry Pi's GPIO to publish message when a button is pressed

### Distance-Monitor.py
Script to measure distance and publish messages is distance is less than 75% of the baseline distance
#### How to use:
place sensor pointing at a hard object like a wall and run script, while the status LED is flashing(around 5 secs) the sensor is taking the baseline distance. When the status LED is solid the script is now monitoring distance and while the distance is 75% or less of the baseline and message will published to AWS IoT Core.

#### Circuit Diagram
```
 +5v------------------------------------
                                |
                               Vcc						 
                          --------------
 GPIO18---------------Trig| Ultrasonic |
 GPIO24---R1----------Echo|   Sensor   |
                   |      --------------
                   |           Gnd
 GPIO26--R1-----   |            |
 GPIO19--R1-   |   R2           |
           |   |   |            |
          LED LED  |            |
           |   |   |            |
 Gnd------------------------------------
 
 R1 = 330 ohm
 R2 = 470 ohm
 Ultrasonic Sensor = HC-SR04 Module
```
