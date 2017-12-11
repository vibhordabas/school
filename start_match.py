import boto3
s3client = boto3.client('s3')
rekogclient = boto3.client('rekognition')

bucket='rekognition-video-console-demo-iad-666698781248-tgccygniptme'
bucket2='attendancebucketbase-vibhordabas'
response = s3client.list_objects_v2(
    Bucket=bucket,
    #Delimiter='string',
    #EncodingType='url',
    #MaxKeys=123,
    Prefix='SMPS',
    #ContinuationToken='string',
    #FetchOwner=True|False,
    #StartAfter='string',
    #RequestPayer='requester'
)


for i in range(len(response['Contents'])):
 key=response['Contents'][i]['Key']
 response2 = rekogclient.search_faces_by_image(
    CollectionId='xxxallfacecollection',
    FaceMatchThreshold=80,
    Image={
        'S3Object': {
            'Bucket': bucket,
            'Name': key,
        },
    },
    MaxFaces=100,
 )
 if len(response2['FaceMatches'])>0:
  print(len(response2['FaceMatches']))
  response3 = s3client.get_object_tagging(
    Bucket=bucket,
    Key=key,
    
	)
  print(response3['TagSet'][0]['Value'])

print('deleting collection')
response4 = rekogclient.delete_collection(CollectionId='xxxallfacecollection')
if response4['StatusCode']==200:
 print('collection deleted : xxxallfacecollection')
 response4 = rekogclient.create_collection(CollectionId='xxxallfacecollection')
 if response4['StatusCode']==200:
  print('Collection created : xxxallfacecollection')
 else:
  print('unable to create collection')
else:
 print('undable to delete collection')

print('Clearing bucket :  ' +bucket2)
'''
response5 = s3client.list_objects_v2(
									Bucket=bucket2,
									Prefix='SMPS',
									)


for i in range(len(response5['Contents'])):
 key=response5['Contents'][i]['Key'] 
 print('Deleting ' + response5['Contents'][i]['Key'] + ' from S3 bucket')
 response6 = s3client.delete_objects(
    Bucket=bucket2,
    Delete={
        'Objects': [
            {
                'Key':key
            },
        ],
        
    },
 )
 if response6['ResponseMetadata']['HTTPStatusCode']==200:
  print('Deleted : '+ key )
'''
import boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket('attendancebucketbase-vibhordabas')
bucket.objects.all().delete()

  

 
 
 
 
