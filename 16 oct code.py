#to notify through email if attendance was marked

from __future__ import print_function
import boto3

print('loading function')

def call_dynamodb(params):
    print ('going to dynamoDB to get name')
    
    dbclient = boto3.client('dynamodb')
    response = dbclient.get_item(
    TableName='testschoolinfo',
    Key={
        'admnum': {						#partition key
                   'N': '1',
				  },
		'externalid': {					#sort key
                   'S': params,
				  },
    },
	AttributesToGet=[
        'name',
    ],
    )
    name=response['Item']['name']['S']
    return name

def notify_parents(para):
    
    print('inside notify_parents')    
    client = boto3.client('sns')
    response = client.publish(
    TargetArn='arn:aws:sns:us-east-1:666698781248:notify_parents',
    Message='Attendance has been marked as' +' PRESENT '+'for your ward.' + para,
    Subject='Attendance Marked',
    MessageStructure='string',
    MessageAttributes={'string': {'DataType': 'String','StringValue': 'String'}})
    print('exiting notify_parents')
    
def check_match(event1):
    
    print('inside check_match')
    rekogclient = boto3.client('rekognition')
    
    bucket_name = event1['Records'][0]['s3']['bucket']['name']
    object_key = event1['Records'][0]['s3']['object']['key']
    
    response = rekogclient.search_faces_by_image(
    CollectionId='xxxallfacecollection',
    FaceMatchThreshold=90.0,
    Image={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': object_key,
        },
    },
    MaxFaces=10,
    )
    if  response['FaceMatches'][0]['Similarity']>90:
        externalid=response['FaceMatches'][0]['Face']['ExternalImageId']
        name=call_dynamodb(externalid)
        return name
    else:
        return 'Face not found in collection'
    print('exiting check_match')
    
def lambda_handler(event,context):
    print('inside handler')
    
#call check_match
    name=check_match(event)
    print (name)
    if name=='Face not found in collection':
        pass
        
    else:
        notify_parents(name)
    
    print('exiting handler')
    