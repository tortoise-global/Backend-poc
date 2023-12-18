
import json
import boto3
import jwt


# from cognitojwt import CognitoJWT


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

    if 'headers' in event:
        headers = event['headers']
        if 'Authorization' in headers:
            access_token = headers['Authorization']

            print("acesstoken", access_token)
            token = access_token[1]

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
            
            # Process the token
            user_info = decode_cognito_token(token)

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
                    #'likecounts': int(request_json['likecounts']),
                    #'commentcounts': int(request_json['commentcounts']),
                    #'postseencount': int(request_json['postseencount']),
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
        
        if http_method == 'DELETE' and route == '/deletepostbypostid':
            if 'queryStringParameters' in event and event['queryStringParameters'] and 'postid' in event['queryStringParameters']:
                item_id= event['queryStringParameters']['postid']
                #item_id = event['pathParameters']['postid']
                table.delete_item(Key={'postid': item_id})
                body = f"Deleted item {item_id}"
                body = json.dumps(body)
                return {
                'statusCode': status_code,
                'body': body,
                'headers': headers
            }

        
        if http_method == 'POST' and route == '/addsignup':
            request_json = json.loads(event['body'])

            data = create_user(request_json["useremail"],request_json["permanentpassword"])

            print("asdfg",data)
            print(type(data))
            body = json.dumps({data})
            # body = data



            return {
                'statusCode': status_code,
                'body': body,
                'headers': headers
            }
        

        if http_method == 'GET' and route == '/get_token':
            # request_json = json.loads(event['body'])
            if 'queryStringParameters' in event and event['queryStringParameters'] and 'username' in event['queryStringParameters'] and 'password' in event['queryStringParameters']:

                username = event['queryStringParameters']['username']
                password = event['queryStringParameters']['password']

                data = get_token(username,password)
                body = json.dumps(data)


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


def create_user(useremail,permanentpassword):


    # Initialize Cognito client
    client = boto3.client('cognito-idp', region_name='us-east-1')  # Replace 'YOUR_REGION' with your AWS region

    # Define parameters for user creation
    user_pool_id = 'us-east-1_EUHla6BwY'  # Replace 'YOUR_USER_POOL_ID' with your Cognito User Pool ID
    user_email = useremail
    permanent_password = permanentpassword

    # Create the user with email as the username and a permanent password
    response = client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=user_email,  # Use email as the username
        UserAttributes=[
            {
                'Name': 'email',
                'Value': user_email
            },
            # Add other user attributes as needed
        ],
        DesiredDeliveryMediums=[
            'EMAIL',  # or 'SMS' if required
        ],
        MessageAction='SUPPRESS',  # Sets the user password without sending a confirmation message
    )

    # Set the permanent password for the user
    client.admin_set_user_password(
        UserPoolId=user_pool_id,
        Username=user_email,
        Password=permanent_password,
        Permanent=True
    )

    print("User created with email as username and permanent password:", response)

    return response
    

def get_token(username,password):

    # Initialize the Cognito client
    client = boto3.client('cognito-idp', region_name='us-east-1')

    # Your user pool ID
    user_pool_id = 'us-east-1_EUHla6BwY'

    # Your client ID from the App settings in Cognito
    client_id = '46aniqlgekeu24ngabc2c682sn'

    # Username and password for authentication
    username = username
    password = password

    # Authenticate the user and retrieve tokens
    try:
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        # Access and refresh tokens
        access_token = response['AuthenticationResult']['AccessToken']
        refresh_token = response['AuthenticationResult']['RefreshToken']
        id_token = response['AuthenticationResult']['IdToken']

        # Print or use the tokens as needed
        print("Access Token:", access_token)
        print("Refresh Token:", refresh_token)
        print("ID Token:", id_token)

        data = {
            "Access Token:":access_token,
            "Refresh Token:":refresh_token,
            "ID Token:":id_token
        }

        return data

    except client.exceptions.NotAuthorizedException as e:
        print("Invalid credentials:", e)
    except client.exceptions.UserNotFoundException as e:
        print("User not found:", e)
    except client.exceptions.UserNotConfirmedException as e:
        print("User not confirmed:", e)
    except Exception as e:
        print("Error:", e)




# def decode_cognito_token(token):
#     # Define the Cognito User Pool ID (replace 'YOUR_USER_POOL_ID' with your actual User Pool ID)
#     user_pool_id = 'us-east-1_EUHla6BwY'

#     try:
#         # Decoding the token using the cognito user pool's public key
#         decoded_token = jwt.decode(token, options={"verify_signature": False})
        
#         # Ensure the token was issued by Cognito
#         if decoded_token['iss'] != f'https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}':
#             raise ValueError("Invalid token issuer")
        
#         # You can access the token claims in the decoded token
#         print("Decoded Token Claims:")
#         print(decoded_token)
#         return decoded_token

#     except jwt.ExpiredSignatureError:
#         print("Token has expired")
#     except jwt.JWTError as e:
#         print(f"JWT Error: {e}")
#     except ValueError as e:
#         print(f"ValueError: {e}")
