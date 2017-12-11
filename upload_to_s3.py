# works like a wonderrrrrrrrrrrr


import glob
import boto3
s3client = boto3.client('s3')

response=glob.glob('C:\\Users\\vidabas\\Desktop\\Cloud\\Notes\\ffmpeg\\*.jpg')
for file in response:
 print (file)
 imagename=file.rsplit('\\',1)
 data = open(file,'rb')
 response = s3client.put_object(
 ACL='public-read-write',
 Body=data,
 Bucket='attendancebucketbase-vibhordabas',
 Key=imagename[1],
 ContentType='image/jpeg'
 )
 if response['ResponseMetadata']['HTTPStatusCode']==200:
  print ('upload successful')
 else:
  print ('upload UNsuccessful')


# now adding a flag file at the end of the image upload process 
 
data = open('C:\\Users\\vidabas\\Desktop\\Cloud\\Notes\\ffmpeg\\ffmpeg\\aaaa.jpg','rb')
response = s3client.put_object(
ACL='public-read-write',
Body=data,
Bucket='attendancebucket-vibhordabas',
Key='aaaa.jpg',
ContentType='image/jpeg'
)
#print (response)
input('press key to start lambda...')


