import boto3
import botocore.exceptions   

def lambda_handler(event, context):
    try:
        x = "Hello"

        print(x)
        

    except botocore.exceptions.ClientError as error:
        raise error
    