import boto3
import os
import random

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    response = {}
    noPics = os.environ['NoPics'].split(",")
    startPics = os.environ['StartPics'].split(",")
    item = client.get_item(
        TableName='Man-Hours',
        Key={
            'Name': {'S' : event['name']}
        })
    try:
        picNo = int(item['Item']['PicNo']['N'])
        cam = int(item['Item']['Cam']['N'])
        if(picNo > int(noPics[cam-1])):
            picNo = 1
    except:
        cam = random.randrange(1, int(os.environ['NoCams']+1))
        picNo = random.randrange(int(startPics[cam-1]), int(noPics[cam-1]))
        client.put_item(
            TableName = 'Man-Hours',
            Item = {
                "Name" : {
                    "S" : event['name']
                },
                "Minutes" : {
                    "N" : "0"
                },
                "Cam" : {
                    "N" : str(cam)
                },
                "PicNo" : {
                    "N" : str(picNo)
                },
                "Affiliation" {
                    "S" : event['affiliation']
                }
            }
        )
    finally:
        response['image'] = str(cam) + "/" + picName(picNo, len(str(picNo)))
        return response

# creates the name of the picture given its identifying number
def picName(num, length):
    name = "IMG_"
    for i in range(length, 4):
        if (i != 4):
            name += "0"
    name += str(num) + ".JPG"
    return name
