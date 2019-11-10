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
    obj_list = {}
    try:
        cont = item['Item']['ContToken']['S']
        if (cont == '-'):
            obj_list = s3_client.list_objects_v2(Bucket = 'four-mile-run', Prefix='img/thumbnail/', MaxKeys=500)
        else:
            obj_list = s3_client.list_objects_v2(Bucket = 'four-mile-run', Prefix='img/thumbnail/', MaxKeys=500, ContinuationToken=cont)
    except:
        obj_list = s3_client.list_objects_v2(Bucket = 'four-mile-run', Prefix='img/thumbnail/', MaxKeys=500)
    minutes = -1
    try: 
        minutes = item['Item']['Minutes']['N']
    except:
        minutes = 0
    if (obj_list['IsTruncated']):
        cont = obj_list['NextContinuationToken']
    else:
        cont = '-'
    client.put_item(
        TableName = 'Man-Hours',
        Item = {
        "Name" : {
                "S" : event['name']
            },
            "Minutes" : {
                "N" : str(minutes)
            },
            "ContToken" : {
                "S" : cont
            },
            "Affiliation" : {
                "S" : event['affiliation']
            }
        }
    )
    key = random.choice(obj_list['Contents'])['Key']
    response['image'] = key[14:]
    return response