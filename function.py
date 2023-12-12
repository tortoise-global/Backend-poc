'''
import json

def lambda_handler(event, context):
    print('Event: ', event)
    response_message = 'Hello, World!'
    
    if event['httpMethod'] == 'GET':

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

'''

import json
import boto3

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = 'bookmark_example'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    body = None
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }

    try:
        http_method, route = event['httpMethod'], event['resource']
        if http_method == 'DELETE' and route == '/bookmark':
            if 'queryStringParameters' in event and event['queryStringParameters'] and 'postid' in event['queryStringParameters']:
                item_id= event['queryStringParameters']['postid']
                #item_id = event['pathParameters']['postid']
                table.delete_item(Key={'postid': item_id})
                body = f"Deleted item {item_id}"
        elif http_method == 'GET' and route == '/bookmark/':
             if 'queryStringParameters' in event and event['queryStringParameters'] and 'postid' in event['queryStringParameters']:
                item_id= event['queryStringParameters']['postid']
                #item_id = event['pathParameters']['postid']
                response = table.get_item(Key={'postid': item_id})
                body = response.get('Item')
        elif http_method == 'GET' and route == '/bookmark':
            response = table.scan()
            body = response.get('bookmark')
        elif http_method == 'PUT' and route == '/bookmark':
            request_json = json.loads(event['body'])
            table.put_item(
                Item={
                    'id': request_json['id'],
                    'postid': request_json['postid'],
                    'userid': request_json['userid']
                }
            )
            body = f"Put item {request_json['id']}"
        elif http_method == 'POST' and route == '/bookmark':
            request_json = json.loads(event['body'])
            table.put_item(
                Item={
                    'id': request_json['id'],
                    'postid': request_json['postid'],
                    'userid': request_json['userid']
                }
            )
            body = request_json
        else:
            raise ValueError(f"Unsupported route: {http_method} {route}")
    except Exception as e:
        status_code = 400
        body = str(e)
    finally:
        body = json.dumps(body)

    return {
        'statusCode': status_code,
        'body': body,
        'headers': headers
    }
