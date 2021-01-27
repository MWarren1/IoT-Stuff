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

### sensor_sim.py
script that takes a csv file and publishes each line of the dataset with a specified delay. to try and simulate an IoT sensor
```
usage: sensor simulator [-h] --dataset DATASET --delay DELAY --topic TOPIC

simulates a IoT sensor by publishing messages from a data set in a csv file

arguments:
  -h, --help         show this help message and exit
  --dataset DATASET  file input(must be csv)
  --delay DELAY      time in seconds between published messages
  --topic TOPIC      topic that messages will get published to, needs to be in quotes
```
#### Example
the follow example uses the csv file called data-set.csv in the present working directory, it will publish to the topic test/test every 5 seconds

python sensor-sim.py --dataset data-set.csv --delay 5 --topic "test/test"
