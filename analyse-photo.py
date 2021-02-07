### analyses photo is a script that doe sthe following
### 1. uploads a photo to an S3 bucker
### 2. gets Rekognition to analyse the photo and provide labels
### 3. adds an entry to a dynamoDB table with url, key_id, epoch time and labels

### Setup - for boto3 module to work you need make sure you have configured your aws credentials,
### a guide cna be found here https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration

import boto3
import time
import argparse # not needed for function

### Start of Functions

# detects labels on photo in S3 bucket
def detect_labels(photo, bucket):

    rek_client=boto3.client('rekognition')

    response = rek_client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10)
    return(response)

# uploads file to an s3 bucket and returns key ID and url
def s3_upload_file(file, bucket, key_path="ROOT"):
 
    s3_resource = boto3.resource('s3')
    keyID = file
    # add epoch time to start of file so it will be unique
    epoch_time = str(time.time())
    keyID = epoch_time +"-"+ file
    # if key_path contains a value then add it to the file as a path
    if key_path  != "ROOT":
        keyID = key_path + keyID
    # upload file to bucket
    s3_resource.meta.client.upload_file(
        Filename=file, Bucket=bucket,
        Key=keyID)
    # generates url
    location = boto3.client('s3').get_bucket_location(Bucket=bucket)['LocationConstraint']
    url = "https://%s.s3-%s.amazonaws.com/%s" % (bucket, location, keyID)
    return(keyID,url,epoch_time)

# put new entry in dynamodb table
def Dyn_DB_Put(dyn_db_table, entry):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(dyn_db_table)
    response = table.put_item(
        Item = entry
        )
    return response
### End of Functions ###

# parse cli switches
parser = argparse.ArgumentParser(prog='analyse-photo.py', description='uploads photo to S3 Bucket and gets Rekognition to label what in in the photo, then adds this to a dynamoDB')
parser.add_argument('--photo', required=True, help='the path to the photo')
parser.add_argument('--bucket', required=True, help='name of bucker to upload files')
parser.add_argument('--db', required=True, help='name of the dynamoDB table put entries')
args = parser.parse_args()
# setting up variables
bucket = args.bucket
dyn_db_table = args.db
file = args.photo

# upload file to s3 bucket
# returns (keyID,url,epoch_time)
s3_response = s3_upload_file(file, bucket)
print ("\n" + file + " was successfully uploaded\n")
# Rek to detect photo in s3 for labels
# returns full json response
rek_response = detect_labels(s3_response[0], bucket)
print("\n" + " analysed by Rekognition\n")

# create new DB entry
entry={
            'key_id': s3_response[0],
            'url': s3_response[1],
            ##### Work out how to epoch and labels as decimals
            'epoch': str(s3_response[2]),
        }

# generate labels as json
detected_labels={}
for label in rek_response['Labels']:
    print ("Label: " + label['Name'] + "\t\tConfidence: " + str(label['Confidence']))
    entry[label['Name']] = str(label['Confidence'])


# put dn entry in to DB
dyn_db_response = Dyn_DB_Put(dyn_db_table, entry)
print ("entry has been added to dynamoDB")
