import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    item = client.get_item(
        TableName='Man-Hours',
        Key={
            'Name': {'S' : event['name']}
        }
    )
    try:
        time = int(float(item['Item']['Minutes']['N']))
    except:
        time = -1
    return {
        'statusCode': 200,
        'time': time    
    }
