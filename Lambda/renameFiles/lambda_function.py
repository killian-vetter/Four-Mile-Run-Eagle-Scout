'''
Take out all the stuff with num and picname and instead choose name based on meta data
Do all the stuff in the buffer instead of /tmp 
create a thumbnail for the image (it will automatically load with the full loading upon request)
'''

import boto3
import uuid
from PIL import Image
from urllib.parse import unquote_plus

client = boto3.client('s3')

def createName(image):
    #use https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html
    exif = image._getexif()
    date = exif[36867]
    comment = exif[37510]
    cam = comment[21:27].decode("utf-8")
    return cam+date.replace(" ","-")+'.JPG'

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        client.download_file(bucket, key, download_path)
        obj = Image.open(download_path)
        name = createName(obj)
        resize_path = '/tmp/{}'.format(name)
        client.upload_file(download_path, 'four-mile-run', 'img/full/'+name)
        obj.thumbnail((1280,720))
        obj.save(resize_path)
        client.upload_file(resize_path, 'four-mile-run', 'img/thumbnail/'+name)
        client.delete_object(Bucket=bucket, Key=key)