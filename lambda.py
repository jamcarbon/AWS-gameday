from uuid import UUID

import boto3
import json
import os
import uuid
from datetime import datetime
from botocore.exceptions import ClientError



def lambda_handler(event, context):
    #Lambda handler for birth of a unicorn.
    
    # Initialise DDB client
    DDB_TABLE = os.environ.get("DYNAMODB_TABLE")
    if DDB_TABLE is None:
        raise ClientError("DYNAMODB_TABLE environment variable is undefined")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(DDB_TABLE)
    
    
    # Create new Unicorn TAG
    unicorn_tag: UUID = str(uuid.uuid4())
    
    # Get today's date for birthday
    unicorn_birthday = datetime.now().strftime("%c")


    # Get unicorn details from event
    event_body = json.loads(event["body"])

    unicorn = {

        "id": unicorn_tag,
        "name": event_body["Name"],
        "weight": event_body["Weight"],
        "birthday": unicorn_birthday,
    }

    # create entry in ddb for newborn unicorn:
    response = register_unicorn(table,unicorn)

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:

        # return generated unicorn tag and name back to user:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "A new unicorn is born!!!",
                }
            ),
        }


def register_unicorn(table,unicorn):
    return table.put_item(Item=unicorn,)
    
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hooray! We have a new unicorn!')
    # }