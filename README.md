# IoT-Stuff
dumping ground for IoT stuff

## Requirments/Setup
the following packages/modules are needed for all these scripts
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
