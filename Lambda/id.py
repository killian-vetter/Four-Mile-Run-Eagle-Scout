import boto3
import random

s3_client = boto3.client('s3')
client = boto3.client('dynamodb')

def lambda_handler(event, context):
    response = {}
    item = client.get_item(
        TableName='Man-Hours',
        Key={
            'Name': {'S' : event['name']}
        })
    minutes = round(float(item['Item']['Minutes']['N']) + event['time']/60, 2)
    picture = event['pic']
    picVotes = client.get_item(
        TableName = 'PictureInfo',
        Key = {
            'Picture' : {'S' : picture}
        }
    )
    
    try :
        newItem = picVotes['Item'] 
    except : 
        newItem = {'Picture' : {'S': picture}}

    for vote in event['votes']:
        try: 
            newItem[vote] = { 'N' : str(1 + int(picVotes['Item'][vote]['N'])) }
        except:
            newItem[vote] = { 'N' : '1' } 
    client.put_item(
        TableName = "PictureInfo",
        Item = newItem
    )
    # Get new picture
    # and get new continuation token
    cont = ''
    obj_list = {}
    try:
        cont = item['Item']['ContToken']['S']
        if (cont == '-'):
            obj_list = s3_client.list_objects_v2(Bucket = 'four-mile-run', Prefix='img/thumbnail/', MaxKeys=250)
        else:
            obj_list = s3_client.list_objects_v2(Bucket = 'four-mile-run', Prefix='img/thumbnail/', MaxKeys=250, ContinuationToken=cont)
    except:
        obj_list = s3_client.list_objects_v2(Bucket = 'four-mile-run', Prefix='img/thumbnail/', MaxKeys=250)
    pic = random.choice(obj_list['Contents'])['Key'][14:]
    if (obj_list['IsTruncated']):
        cont = obj_list['NextContinuationToken']
    else:
        cont = '-'

    item2Send = item['Item']
    item2Send['Minutes']['N'] = str(minutes)
    item2Send['ContToken']['S'] = cont
    client.put_item(
        TableName = 'Man-Hours',
        Item = item2Send 
    )
    response['image'] = pic
    return response