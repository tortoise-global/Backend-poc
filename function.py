import json

def lambda_handler(event, context):
    print('Event: ', event)
    response_message = 'Hello, World!'

    if 'queryStringParameters' in event and event['queryStringParameters'] and 'Name' in event['queryStringParameters']:
        response_message = 'Hello, ' + event['queryStringParameters']['Name'] + '!'

    if event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        response_message = 'Hello, ' + body['name'] + '!'

    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'message': response_message
        })
    }

    return response

