'''
Take out all the stuff with num and picname and instead choose name based on meta data
Do all the stuff in the buffer instead of /tmp 
create a thumbnail for the image (it will automatically load with the full loading upon request)
'''

import boto3
from PIL import Image
from urllib.parse import unquote_plus

client = boto3.client('s3')

def createName(image):
    #use https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html
    exif = image._getexif()
    date = exif[36867]
    comment = exif[37510]
    cam = comment[21:27]
    return date.replace(" ","-")+can+'.JPG'

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        obj = Image.read(client.get_record(Bucket=bucket, Key=key))
        # resize picture and save in two different folders img/full and img/thumbnail
        name = createName(obj)
        client.put_object(Bucket='four-mile-run', Key='img/full/'+name, Body=obj)
        obj.thumbnail((1280,720))
        client.put_object(Bucket='four-mile-run', Key='img/thumbnail/'+name, Body=obj)
        client.delete_object(Bucket=bucket, Key=key)