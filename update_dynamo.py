import glob
import boto3

response=glob.glob('C:\\Users\\vidabas\\Desktop\\Cloud\\Notes\\ffmpeg\\*.mp4')
for file in response:
 print (file)
 videoname=file.rsplit('\\',1)


print('inside collect_video')
rekogclient = boto3.client('rekognition')
    
print('starting to search faces in a video')
        
response = rekogclient.start_face_search(
        Video={
        'S3Object': {'Bucket': 'attendancebucketbase-vibhordabas',
                     'Name': videoname[1]
                    }
                    },
        CollectionId='xxxallfacecollection',
        JobTag='facematch1'
        )
        
job_id=response['JobId']
print(response['JobId'])
x=1
next_token=''
E_list=[]
count=0
a=[]
    
while(x):
 response = rekogclient.get_face_search(
                JobId=job_id,  
                NextToken=next_token,
                SortBy='INDEX')
 if 'NextToken' in response:
  next_token=response['NextToken']
 else:
  x=0
for i in range(len(response['Persons'])):
  a=response['Persons'][i]['Person']
  if 'Face' in a and 'Index' in a and 'FaceMatches' in response['Persons'][i] and len(response['Persons'][i]['FaceMatches'])>0:
   count+=1
   admnum=response['Persons'][i]['FaceMatches'][0]['Face']['ExternalImageId']
   E_id=admnum
   if E_id in E_list:
    pass
   else:
    E_list.append(E_id)

#pass the list to dynamoDB

print ('going to dynamoDB to get name')
print(E_list)
dbclient = boto3.client('dynamodb')
for i in range(len(E_list)):
 response = dbclient.get_item(
    TableName='schooldata',
    Key={
        'admnum': {						#partition key
                   'N': E_list[i],
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
                'N': E_list[i], 
            },
        },
        ReturnValues='UPDATED_NEW',  # check its relevance
        TableName='schooldata',
        UpdateExpression='SET oct232017 = :s',  #have to customize this
        )
  print(name)
    
 else :
  print(attendance)    

input("press a key..")















