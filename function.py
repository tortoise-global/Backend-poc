
import json
import boto3

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = 'post'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    body = None
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }

    # try:
    if 1:
        http_method, route = event['httpMethod'], event['resource']

        # #delete post by postid
        # if http_method == 'DELETE' and route == '/post':
        #     if 'queryStringParameters' in event and event['queryStringParameters'] and 'postid' in event['queryStringParameters']:
        #         item_id= event['queryStringParameters']['postid']
        #         #item_id = event['pathParameters']['postid']
        #         table.delete_item(Key={'postid': item_id})
        #         body = f"Deleted item {item_id}"
        #         return {
        #         'statusCode': status_code,
        #         'body': body,
        #         'headers': headers
        #     }

        # #get post by postid
        # elif http_method == 'GET' and route == '/post':
        #      if 'queryStringParameters' in event and event['queryStringParameters'] and 'postid' in event['queryStringParameters']:
        #         item_id= event['queryStringParameters']['postid']
        #         #item_id = event['pathParameters']['postid']
        #         response = table.get_item(Key={'postid': item_id})
        #         body = response
        #         return {
        #         'statusCode': status_code,
        #         'body': body,
        #         'headers': headers
        #     }

        #get all post        
        if http_method == 'GET' and route == '/allpost':
            response = table.scan()
            body = response.get('Items')
            body = json.dumps(body)
            print("hey im printing body",body)
            return {
                'statusCode': status_code,
                'body': body,
                'headers': headers
            }
        #create post
        elif http_method == 'POST' and route == '/addpost':
            request_json = json.loads(event['body'])
            table.put_item(
                Item={
                    'id': request_json['id'],
                    'postid': request_json['postid'],
                    'studentid': request_json['studentid'],
                    'title': request_json['title'],
                    'body': request_json['body'],
                    'mediacontent': request_json['mediacontent'],
                    'creationdate': request_json['creationdate'],
                    'likecounts': request_json['likecounts'],
                    'commentcounts': request_json['commentcounts'],
                    'postseencount': request_json['postseencount'],
                    'tags': request_json['tags'],
                    'professionalid': request_json['professionalid']
                }
            )
            body = request_json
            body = json.dumps(body)
            return {
                'statusCode': status_code,
                'body': body,
                'headers': headers
            }
        # # update post
        # elif http_method == 'PUT' and route == '/post':
        #     request_json = json.loads(event['body'])
        #     table.put_item(
        #          Item={
        #             'id': request_json['id'],
        #             'postid': request_json['postid'],
        #             'studentid': request_json['studentid'],
        #             'title': request_json['title'],
        #             'body': request_json['body'],
        #             'mediacontent': request_json['mediacontent'],
        #             'creationdate': request_json['creationdate'],
        #             'likecounts': request_json['likecounts'],
        #             'commentcounts': request_json['commentcounts'],
        #             'postseencount': request_json['postseencount'],
        #             'tags': request_json['tags'],
        #             'professionalid': request_json['professionalid'],
        #             # 'studentdata': request_json['studentdata']
        #         }
        #     )
        #     body = f"Put item {request_json['id']}"
        #     return {
        #         'statusCode': status_code,
        #         'body': body,
        #         'headers': headers
        #     }

        # create post
       
    #     else:
    #         raise ValueError(f"Unsupported route: {http_method} {route}")
    # except Exception as e:
    #     status_code = 400
    #     body = str(e)
    #     body = json.dumps(body)

    # finally:
    #     body = json.dumps(body)

    # return {
    #     'statusCode': status_code,
    #     'body': body,
    #     'headers': headers
    # }




