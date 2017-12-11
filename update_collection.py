import boto3
s3client = boto3.client('s3')
rekogclient = boto3.client('rekognition')

bucket='attendancebucketbase-vibhordabas'

response = s3client.list_objects_v2(
    Bucket=bucket,
    Prefix='SMPS',
    #ContinuationToken='string',
    )

for i in range(len(response['Contents'])):
 key=response['Contents'][i]['Key'] 
 print(response['Contents'][i]['Key'])
 response2 = rekogclient.index_faces(
    CollectionId='xxxallfacecollection',
    Image={
            'S3Object': {
            'Bucket': bucket,
            'Name': key
            
        }
    },
 )
 
