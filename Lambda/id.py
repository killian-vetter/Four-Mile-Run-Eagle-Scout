import boto3
import os
import re

client = boto3.client('dynamodb')
#s3client = boto3.client('s3')

def lambda_handler(event, context):
    response = {}
    noPics = os.environ['NoPics'].split(",")
    item = client.get_item(
        TableName='Man-Hours',
        Key={
            'Name': {'S' : event['name']}
        })
    minutes = float(item['Item']['Minutes']['N']) + event['time']
    picInfo = isValidPhoto(event['pic'])
    if (picInfo is None):
        return item['Item']['Cam']['N']+"/"+picName(item['Item']['PicNo']['N'],len(item['Item']['PicNo']['N']))
    cam = picInfo['cam']
    picNo = picInfo['picNo']
    picVotes = client.get_item(
        TableName = 'PictureInfo',
        Key = {
            'PicNo' : {'N' : str(picNo)},
            'Cam' : {'N' : str(cam)}
        }
    )
    newItem = {
        'PicNo' : {'N' : str(picNo)},
        'Cam' : {'N' : str(cam)}
    }
    for vote in event['votes']:
        try: 
            newItem[vote] = { 'N' : str(1 + int(picVotes['Item'][vote]['N'])) }
        except:
            newItem[vote] = { 'N' : '1' } 
    client.put_item(
        TableName = "PictureInfo",
        Item = newItem
    )
    picNo += 1
    if (picNo > int(noPics[cam-1])):
        picNo = 1
    client.put_item(
        TableName = 'Man-Hours',
        Item = {
            "Name" : {
                'S' : event['name']
            },
            "Minutes" : {
                'N' : str(minutes)
            },
            "PicNo" : {
                'N' : str(picNo)
            },
            "Cam" : {
                'N' : str(cam)
            }
        }
    )
    pic = str(cam) + "/" + picName(picNo, len(str(picNo)))
    response['image'] = pic
    return response

# creates the name of the picture given its identifying number
def picName(num, length):
    name = "IMG_"
    for i in range(length, 4):
        if (i != 4):
            name += "0"
    name += str(num) + ".JPG"
    return name

def isValidPhoto(name):
    response = {}
    arr = name.split("/")
    if len(arr) == 2 and (arr[0] == '1' or arr[0]=='2') and re.match("IMG_....(\.)JPG", arr[1]) is not None: 
       response['picNo'] = int(arr[1][4:8])
       response['cam'] = int(arr[0])
       return response
    else:
        return None