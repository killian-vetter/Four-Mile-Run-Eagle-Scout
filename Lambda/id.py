import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    response = {}
    item = client.get_item(
        TableName='Man-Hours',
        Key={
            'Name': {'S' : event['name']}
        })
    minutes = round(float(item['Item']['Minutes']['N']) + event['time'], 2)
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
    pic = ''

    item2Send = item['Item']
    item2Send['Minutes']['N'] = str(minutes)
    client.put_item(
        TableName = 'Man-Hours',
        Item = item2Send 
    )
    response['image'] = pic
    return response