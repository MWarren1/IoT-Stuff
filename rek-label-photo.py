### Rek-Label-Photo
### uploads photo to Rekognition and prints labels

import boto3
import argparse # not needed for function

### Start of Functions ###
def detect_labels_local_file(photo):


    client=boto3.client('rekognition')

    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})

    return (response)
### End of Functions ###

# parse cli switches
parser = argparse.ArgumentParser(prog='rek-label-photo.py', description='uses AWS Rekognition to label what in in the photo')
parser.add_argument('--photo', required=True, help='this is the path to the photo')
args = parser.parse_args()

photo=args.photo
# sent photo to rek
response = detect_labels_local_file(photo)
# count number of labels detected
label_count= len(response['Labels'])

# print all labels
print('Detected labels in ' + photo)
for label in response['Labels']:
    print (label['Name'] + ' : ' + str(label['Confidence']))

print("Labels detected: " + str(label_count))
