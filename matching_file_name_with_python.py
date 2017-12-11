# works like a wonderrrrrrrrrrrr


import glob
import boto3
s3client = boto3.client('s3')

response=glob.glob('C:\\Users\\vidabas\\Desktop\\Cloud\\Notes\\ffmpeg\\*.jpg')
for file in response:
	print (file)
	data = open(file,'rb')
	response = s3client.put_object(
	ACL='public-read-write',
	Body=data,
	Bucket='attendancebucket-vibhordabas',
	Key=file,
	ContentType='image/jpeg'
	)
	



