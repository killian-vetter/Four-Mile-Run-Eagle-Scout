'''
Take out all the stuff with num and picname and instead choose name based on meta data
Do all the stuff in the buffer instead of /tmp 
create a thumbnail for the image (it will automatically load with the full loading upon request)
'''

import boto3

client = boto3.client('s3')

def picName(num, length):
    name = "IMG_"
    for i in range(length, 4):
        if (i != 4):
            name += "0"
    name += str(num) + ".JPG"
    return name

def lambda_handler(event, context): 
    num = int(client.get_object(
        Bucket = "four-mile-run",
        Key = "num.txt")['Body'].read().decode('utf-8'))

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path = '/img/'+ picName(num, len(num))
        client.download_file(bucket, key, download_path)
        client.upload_file(upload_path, "four-mile-run", picName(num, len(num)))
        num = num + 1

    client.download_filobj("four-mile-run", "num.txt", str(num).encode())