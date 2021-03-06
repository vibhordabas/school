#to notify through email if attendance was marked
import os
import os.path
import sys
root = os.environ["LAMBDA_TASK_ROOT"]
sys.path.insert(0, root)
import boto3
from __future__ import print_function
print('loading function')
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------
'''
def send_sms():
    auth_id = "MAMTBIMDYZZGZKMZU5MT"	
    auth_token = "YzViNzA2ZTk3OTk1NjcyOTI2NjA1OTFjZDU3MzUz"
    p = plivo.RestAPI(auth_id, auth_token)
    
    params = {
        'src': '917760054004', 
        'dst' : '+918010453417', 
        'text' : u"Hello, this is vibhor testing plivo."
    }
    response = p.send_message(params)
'''

def notify_parents_absent():
    
    print('inside notify_parents_absent')    
    client = boto3.client('sns')
    
    dbclient = boto3.client('dynamodb')
    response = dbclient.scan(
    Select='ALL_ATTRIBUTES',
    TableName='schooldata',
        ExpressionAttributeValues={
            ':a': {
                'S': 'n',
            },
        },
    FilterExpression='oct232017 = :a')
    
    namelist=[]
    for keys in range(len(response['Items'])):
     for dict1 in response['Items'][keys]:
      if dict1=='name':
       for name in response['Items'][keys][dict1]:
        namelist.append(response['Items'][keys][dict1][name])
    print(namelist)
    
    for name in range(len(namelist)):
        response = client.publish(
        TargetArn='arn:aws:sns:us-east-1:666698781248:notify_parents_absent',
        Message='Attendance has been marked as' +' ABSENT '+'for your ward.' + namelist[name],
        Subject='Attendance Marked',
        MessageStructure='string',
        MessageAttributes={'string': {'DataType': 'String','StringValue': 'String'}})
    
    print('exiting notify_parents_absent')

#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------

def notify_parents_present(para):
    
    print('inside notify_parents')    
    client = boto3.client('sns')
    response = client.publish(
    TargetArn='arn:aws:sns:us-east-1:666698781248:notify_parents',
    Message='Attendance has been marked as' +' PRESENT '+'for your ward.' + para,
    Subject='Attendance Marked',
    MessageStructure='string',
    MessageAttributes={'string': {'DataType': 'String','StringValue': 'String'}})
    print('exiting notify_parents')
    
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------

def call_dynamodb1(params):
    print ('going to dynamoDB to get name')
    print(params)
    dbclient = boto3.client('dynamodb')
    response = dbclient.get_item(
    TableName='schooldata',
    Key={
        'admnum': {						#partition key
                   'N': params,
				  },
    },
	AttributesToGet=[
        'name','oct232017'  #hardcoded
    ],
    )
    name=response['Item']['name']['S']
    attendance=response['Item']['oct232017']['S'] #column has to created for everyday
    print ('attendance : '+ attendance)
    if attendance=='n':
        print('attendance not marked ! ')
        response = dbclient.update_item(
        ExpressionAttributeValues={
            ':s': {
                'S': 'p',
            }
        },
        Key={
            'admnum': {
                'N': params, 
            },
        },
        ReturnValues='UPDATED_NEW',  # check its relevance
        TableName='schooldata',
        UpdateExpression='SET oct232017 = :s',  #have to customize this
        )
        return name
    
    else :
        return attendance    

#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------

'''
def check_match1():
    
    print('inside check_match1')
    rekogclient = boto3.client('rekognition')
    
    s3client = boto3.client('s3')
    paginator = s3client.get_paginator('list_objects_v2')

    response_iterator = paginator.paginate(
                        Bucket='attendancebucketbase-vibhordabas',
                        #Prefix='SMPS',                                      #not to bbe hardcoded
                        #StartAfter='string',
                        #RequestPayer='requester',
                        PaginationConfig={
                                        'MaxItems': 1000,
                                        'PageSize': 1000,
                                        #'StartingToken': 'string'
                                        }
                        )

    for page in response_iterator:
        #print (page['Contents'])
        for content in range(len(page['Contents'])):
            #print(page['Contents'][content])
            keyli=page['Contents'][content]
            print(keyli['Key'])
        
            response = rekogclient.search_faces_by_image(
            CollectionId='xxxallfacecollection',
            FaceMatchThreshold=85.0,
            Image={
                'S3Object': {
                    'Bucket': 'attendancebucketbase-vibhordabas',
                    'Name': keyli['Key'],
                },
            },
            MaxFaces=10,
            )
            if  len(response['FaceMatches'])>0 and (response['FaceMatches'][0]['Similarity']>85):
                response = s3client.get_object_tagging(
                Bucket='attendancebucketbase-vibhordabas',
                Key=keyli['Key']
                )
                admnum=response['TagSet'][0]['Value']
                print('calling dynamodb1')
                reply_from_db=call_dynamodb1(admnum)
                
                if reply_from_db=='p':
                    print("attendance already marked")
                else:
                    notify_parents_present(reply_from_db)
            
            else:
                print('Face not matched in collection')
                
    print('exiting check_match1')
'''
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------


def collect_video(event1):
    print('inside collect_video')
    rekogclient = boto3.client('rekognition')
    
    print('starting to search faces in a video')
        
    response = rekogclient.start_face_search(
        Video={
        'S3Object': {'Bucket': bucket_name,
                     'Name': object_key
                    }
                    },
        CollectionId='xxxallfacecollection',
        JobTag='facematch'
        )
        
    job_id=response['JobId']
    x=1
    next_token=''
    
    while(x):
     response = client.get_face_search(
                JobId=job_id,  
                NextToken=next_token,
                SortBy='INDEX')
     if 'NextToken' in response:
      next_token=response['NextToken']
     else:
      x=0
    
    count=0
    a=[]
    for i in range(len(response['Persons'])):
     a=response['Persons'][i]['Person']
     if 'Face' in a and 'Index' in a and 'FaceMatches' in response['Persons'][i] and len(response['Persons'][i]['FaceMatches'])>0:
      count+=1
      admnum=response['Persons'][i]['FaceMatches'][1]['Face']['ExternalImageId']
      print(response['Persons'][i]['FaceMatches'][1]['Face']['ExternalImageId']  )

    
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------

def lambda_handler(event,context):
    print('inside handler')
    

    collect_video(event)
    
    
    #send_sms()
    '''
    reply_from_db=check_match(event)
    print (reply_from_db)
    if reply_from_db=='Face not found in collection':
        pass
    
    elif reply_from_db=='p':
        print("attendance already marked")
    
    else:
        notify_parents(reply_from_db)
        
    print('exiting handler')
    '''
    
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------


