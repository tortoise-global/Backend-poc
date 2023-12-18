# from cognitojwt import CognitoJWT
# from cognitojwt.jwt_client import CognitoJWT

from pycognito import Cognito
import jwt

token = "eyJraWQiOiJicTRDbkhhWG91VDJISURsd3h4enMzNURFclBWMHRKRDBwcjFpSzRqUDMwPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJkZjYxYzI2ZS0yZDYxLTRhMmYtOGU4ZS0xZTdkMGNhOTZhYzYiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9FVUhsYTZCd1kiLCJjbGllbnRfaWQiOiI0NmFuaXFsZ2VrZXUyNG5nYWJjMmM2ODJzbiIsIm9yaWdpbl9qdGkiOiJiNjQxMmQxYi1jNmJiLTRiMDAtODhiOS0wZjlkYTk2Yzk0ZTAiLCJldmVudF9pZCI6IjJlMTI3NDJiLWQxYTYtNDE3ZC05NGU4LTlmOTJjZDQwNjg4ZSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3MDI5MDg0ODYsImV4cCI6MTcwMjkxMjA4NiwiaWF0IjoxNzAyOTA4NDg2LCJqdGkiOiI2MjhhZTNkYi1kMmQ2LTRlYjgtYThjNy1jMjgxMGU3YThhZWYiLCJ1c2VybmFtZSI6ImRmNjFjMjZlLTJkNjEtNGEyZi04ZThlLTFlN2QwY2E5NmFjNiJ9.Gjz-nX0ZNggmckUkLWWtC9ZFaecouR6wdX_uC_vAlvF0xL3xR3VmetR2R8xTDlbjpAtAiR2A9uJdshghiCcI-jfAZG9Tvg89d7-dBSSLtKf4ePa3Pl4f3_8WjmWUSzKFc2ZGVjM7kyEG3yiHpmayc_sfPQ1z8F0oIsvRaSY-6YKdKBJGzFSmwBIluOC0gfdDC6MqpDtMXOpXPcgyUzBqAmJkTjh81v-DcuszTl2V6ycZ7gHT2eiqp64PoBdueHA-FijkO9UsXeLuOT4aLpKt3WoDJf1HtvNPlAUMFPrpymvZzpkAO-fXhOFYjbPIko0RnyiXFmgQK-73MapzL0V2ag"

def authenticate_cognito_token(token):

    user_pool_id = "us-east-1_EUHla6BwY"
    region_name='us-east-1'

    payloaddata = jwt.decode(token,options={"verify_signature": False})

    print(payloaddata)
    return payloaddata
    # print(token)
    
    # u = Cognito('us-east-1_EUHla6BwY','46aniqlgekeu24ngabc2c682sn',
    # id_token='id-token',refresh_token='refresh-token',
    # access_token='access-token')

    # u = Cognito('us-east-1_EUHla6BwY','46aniqlgekeu24ngabc2c682sn',
    # access_token=token)

    # print(u)

    # u.check_token()
    # u.verify_tokens()

    # print("sdfgh",u.verify_tokens())
    

   #Replace with your Cognito User Pool ID
   
   
    # # Initialize CognitoJWT object
    # cognito_jwt = CognitoJWT(token, user_pool_id, region)

    # try:
    #     # Verify the token
    #     claims = cognito_jwt.verify()

    #     print("sdfghj",claims)
        
    #     # Access claims (user information)
    #     # user_id = claims['username']
    #     email = claims['email']
    #     # Add more claims as needed

    #     # Token is valid, return user information
    #     return {
    #         # 'user_id': user_id,
    #         'email': email,
    #         # Add more user information as needed
    #     }
    # except Exception as e:
    #     # Token verification failed
    #     print(f"Token verification failed: {str(e)}")
    #     return None

# # Example usage
# access_token = 'YOUR_COGNITO_ACCESS_TOKEN'  # Replace with your Cognito access token
# user_info = authenticate_cognito_token(access_token)

# if user_info:
#     print("Token is valid.")
#     print("User ID:", user_info['user_id'])
#     print("Email:", user_info['email'])
#     # Access more user information as needed
# else:
#     print("Token is invalid.")
authenticate_cognito_token(token)


import jwt

def decode_cognito_token(token):
    # Define the Cognito User Pool ID (replace 'YOUR_USER_POOL_ID' with your actual User Pool ID)
    user_pool_id = 'YOUR_USER_POOL_ID'

    try:
        # Decoding the token using the cognito user pool's public key
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        
        # Ensure the token was issued by Cognito
        if decoded_token['iss'] != f'https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}':
            raise ValueError("Invalid token issuer")
        
        # You can access the token claims in the decoded token
        print("Decoded Token Claims:")
        print(decoded_token)
        return decoded_token

    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.JWTError as e:
        print(f"JWT Error: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")

# Example token (replace this with your actual token)
access_token = 'YOUR_ACCESS_TOKEN'

# Decode the provided Cognito access token
decode_cognito_token(access_token)
