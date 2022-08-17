import boto3
import os

# s3 = boto3.resource('s3')

# # print out bucket names
# for bucket in s3.buckets.all():
#     print(bucket.name)

# #upload a new file
# data = open('raw_data/ikeadata.json', 'rb')
# s3.Bucket('ikeascraper').put_object(Key='raw_data/ikeadata.json', Body=data)

def upload_files(path):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('ikeascraper')
 
    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                bucket.put_object(Key=full_path, Body=data)
    
    print('upload complete')
 
if __name__ == "__main__":
    upload_files('raw_data/')
