"""
This lambda function gets the token from Amazon Cognito. 
Then invokes the API GW with the imbedded authorization token.
"""
import json
import boto3
import requests
import logging

# It is a good practice to use proper logging.
# Here we are using the logging module of Python.
# https://docs.python.org/3/library/logging.html

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# For training purposes, you are adding clear text credentials. 
# As a standard practice, the credentials are saved in the AWS Secrets Manager.

user_pool_id = 'us-east-1_2YlfQB9yi'
client_id = '1suhpsokjrhmkhefagatpklo97'
user_name = 'maltino'
password = 'Umasenha123!'
api_gateway_url = 'https://uzkjlsns9f.execute-api.us-east-1.amazonaws.com/prod/diy'

def lambda_handler(event, context):
    logging.info(event)
   
    client = boto3.client('cognito-idp')
    response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': user_name,
                'PASSWORD': password
            }
        )
    token = response['AuthenticationResult'].get('IdToken')
    logging.info(token)

    ## Uncomment below line to invoke API GW with the authorization token.
    access_api(token)
    return response
    
def access_api(token):
    
    auth_token=str(token)
    header = {'Authorization': auth_token}
    print(header)
    
    url = api_gateway_url
    response = requests.get(url,headers=header)
    logger.info(response)
    
    for item in response:
        logger.info(item)
