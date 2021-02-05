### Rek-Detect-Mask
### detects how many people in a photo and how many  are wearing masks

import boto3
import argparse # Not needed for the functions


### Start of Functions###

# uploads local photo to Rekognition and returns the response
def rek_detect_mask(photo, minconfidence):

    client=boto3.client('rekognition')

    with open(photo, 'rb') as image:
        response = client.detect_protective_equipment(Image={'Bytes': image.read()}, 
            SummarizationAttributes={'MinConfidence':minconfidence, 'RequiredEquipmentTypes':['FACE_COVER']})     
    return (response)

#Display summary information for supplied summary.
def rek_mask_display_summary(summary_type, summary):
    print (summary_type + '\n\tIDs: ',end='')
    if (len(summary)==0):
        print('None')
    else:
        for num, id in enumerate(summary, start=0):
            if num==len(summary)-1:
                print (id)
            else:
                print (str(id) + ', ' , end='')

# lists all people and if they are wearing a face mask
def rek_resp_mask_details(response):

    print('\nFace masks detected in image ' + photo) 
    print('\n---------------\nDetected people\n---------------')   
    for person in response['Persons']: 
        print('Person ID: ' + str(person['Id']))
        body_parts = person['BodyParts']
        if len(body_parts) == 0:
            print ('No body parts found')
        else:
            for body_part in body_parts:
                if body_part['Name'] == 'FACE':
                    ppe_items = body_part['EquipmentDetections']
                    if len(ppe_items) ==0:
                        print ('\tNo Face Mask detected')
                    else:    
                        for ppe_item in ppe_items:
                            print('\t' + ppe_item['Type'] + '\tConfidence: ' + str(ppe_item['Confidence']))
    return()

# uses response from rek
def rek_resp_mask_summary(response):
    total_people = 0
    people_mask = 0
    for person in response['Persons']:
        total_people = total_people + 1    
        body_parts = person['BodyParts']
        if len(body_parts) >= 1:
            for body_part in body_parts:
                if body_part['Name'] == 'FACE':
                    ppe_items = body_part['EquipmentDetections']
                    if len(ppe_items) >= 1: 
                        people_mask = people_mask + 1
    return(people_mask, total_people)
### End of Function ###

# parse cli switches
parser = argparse.ArgumentParser(prog='rek-detect-mask', description='uses AWS Rekognition to detect face masks in photos')
parser.add_argument('--photo', required=True, help='this is the path to the photo')
args = parser.parse_args()


photo=args.photo
# sent photo to rek and get response
response=rek_detect_mask(photo, 80)

# print details of the rek'd response
rek_resp_mask_details(response)

# get and print number of people in masks and total people
people = rek_resp_mask_summary(response)
print('\n----------------\n    Summary\n----------------')
print(str(people[0]) + ' person/s out of ' + str(people[1]) + ' in the photo are wearing a mask\n----------------')

