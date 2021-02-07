# IoT-Stuff
dumping ground for IoT stuff

## Requirments/Setup
### AWS IoT Core setup
the following packages/modules are needed for all these scripts that involve AWS IoT Core. Run the following commands to install:
* sudo apt-get install cmake
* sudo apt-get install libssl-dev
* sudo pip install awsiotsdk

also you will need to register your device with AWS IoT and the all your aws variables need to be added to awsconfig.py

### AWS Rekognition setup
the following module is needed for python, i recommend using python 3 for these scripts. Run the following commands to install:
* sudo python3 -m pip install boto3

you will also need to generate a access key ID and an access key secret on AWs for the scripts to use. instructions on where to put these can be found here:
https://docs.aws.amazon.com/rekognition/latest/dg/setup-awscli-sdk.html 

## AWS IoT Core Scripts

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


## AWS Rekognition Scripts

### rek-label-photo.py
script that uploads a local photo to AWS Rekognition and prints all labels that Rekognition detected

```
usage: rek-label-photo.py [-h] --photo PHOTO

uses AWS Rekognition to label what in in the photo

optional arguments:
  -h, --help     show this help message and exit
  --photo PHOTO  this is the path to the photo
```

### rek-detect-mask.py
script that uploads local photo and detect the number of people and if they are wearing face masks

```
usage: rek-detect-mask.py [-h] --photo PHOTO

uses AWS Rekognition to detect face masks in photos

optional arguments:
  -h, --help     show this help message and exit
  --photo PHOTO  this is the path to the photo
```

### analyse-photo.py
analyses photo is a script that does the following:
1. uploads a photo to an S3 bucket
2. gets Rekognition to analyse the photo and provide labels
3. adds an entry to a dynamoDB table with url, key_id, epoch time and labels

```
usage: analyse-photo.py [-h] --photo PHOTO --bucket BUCKET --db DB

uploads photo to S3 Bucket and gets Rekognition to label what in in the photo, then adds this to a dynamoDB

optional arguments:
  -h, --help       show this help message and exit
  --photo PHOTO    the path to the photo
  --bucket BUCKET  name of bucket to upload files
  --db DB          name of the dynamoDB table put entries
```
