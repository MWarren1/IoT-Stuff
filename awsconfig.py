import os

### Following variables need to be defined
# Define ENDPOINT, CLIENT_ID
CLIENT_ID = os.popen('hostname').readline().strip('\n') # This grabs the hostname but can be replaced witha string
ENDPOINT = "<PUT YOUR ENDPOINT HERE>"

# Paths to Amazon CA, Private cert and key
PATH_TO_CERT = "<PUT THE PATH TO YOUR CERT HERE>"
PATH_TO_KEY = "<PUT THE PATH TO YOUR KEY HERE>"
PATH_TO_ROOT = "<PUT THE PATH TO AMAZON CA HERE>"
