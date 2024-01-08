
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
    token = None
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }

    if 'headers' in event:
        headers = event['headers']
        if 'Authorization' in headers:
            access_token = headers['Authorization']

            print("acesstokensdfg", access_token)
            token = access_token[1]
            print("mytoken",token)

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

            print("from user",user_info)

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
                    # 'likecounts': {"N":request_json['likecounts']},
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



        if http_method == 'POST' and route == '/sendemail':
            request_json = json.loads(event['body'])

            # data = create_user(request_json["useremail"],request_json["permanentpassword"])

            otp = generateOTP()

            if request_json['email']:
                subject = 'TURTIL'
                aws_response = email_service(request_json['email'],subject,request_json['messagetype'],request_json['apptype'],otp)
                print("email",aws_response)
            
            else:

                aws_response = {}

                aws_response:"please_enter_your_email"


            print("asdfg",data)
            print(type(data))
            body = json.dumps({aws_response})
            # body = data



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




def decode_cognito_token(token):
    # Define the Cognito User Pool ID (replace 'YOUR_USER_POOL_ID' with your actual User Pool ID)
    # user_pool_id = 'us-east-1_EUHla6BwY'

    try:

        user_pool_id = "us-east-1_EUHla6BwY"

        payloaddata = jwt.decode(token,options={"verify_signature": False})

        print(payloaddata)
        return payloaddata
        # Decoding the token using the cognito user pool's public key
        # decoded_token = jwt.decode(token, options={"verify_signature": False})
        
        # # Ensure the token was issued by Cognito
        # if decoded_token['iss'] != f'https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}':
        #     raise ValueError("Invalid token issuer")
        
        # # You can access the token claims in the decoded token
        # print("Decoded Token Claims:")
        # print(decoded_token)
        # return decoded_token

    except jwt.ExpiredSignatureError:
        print("Token has expired")
    # except jwt.JWTError as e:
    #     print(f"JWT Error: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")

    except Exception as e:
        print("Error:", e)
        return e



#hello world

# common functions
def generateOTP():
    import math
    import random
    digits = "1234567891"
    OTP = ""
    for i in range(5):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP



def email_service(to_address,subject,messagetype,apptype,otp):

    import os
    import boto3
    from botocore.exceptions import ClientError
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication

    SENDER = "karthik@iconsoftwareinc.com"

    RECIPIENT = to_address

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "ap-south-1"

    # The subject line for the email.
    SUBJECT = subject.upper()
    # sendfrom = "EMAIL"

    # body = message_template_for_forgot_password(messagetype,apptype,otp,sendfrom)

    # print("hey"+body)

    
    if messagetype == 'OTP':
        # body = "Your OTP for "+apptype.upper()+" is "+otp +' \nThank you \nVISEPL'
        body = """\
        <!DOCTYPE html>
        <html>
        <body>
        <p>Your OTP for """+apptype.upper()+""" is <span style="text-decoration: underline">"""+otp+"""</span> </p>
        <p>Thank you, <br/> TURTIL.</p>

        </body>
        </html>
        """
    

    # The HTML body of the email.
    BODY_HTML = """\
    <html>
    <head></head>
    <body>
    <p>""" + body + """</p>
    </body>
    </html>
    """
   

    # The character encoding for the email.
    CHARSET = "utf-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')

    # Add subject, from and to lines.
    msg['Subject'] = SUBJECT 
    msg['From'] = SENDER 
    msg['To'] = RECIPIENT

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

    # Add the text and HTML parts to the child container.
    msg_body.attach(htmlpart)

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    try:
        response = client.send_raw_email(Source=SENDER,Destinations=[RECIPIENT],RawMessage={'Data':msg.as_string(),},)
        return response

    except ClientError as e:
        print(e.response['Error']['Message'])
    # else:
    #     print("Email sent! Message ID:"),
    #     print(response['MessageId'])
    
    # return response