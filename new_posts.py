import boto3
import os
import uuid 
import json

def lambda_handler(event, context):
    recordId = str(uuid.uuid4())
    voice = event["voice"]
    text = event["text"]
    
    print('Generating new Dynamo Db record, with ID: ' + recordId) 
    print('Input Text: ' + text)
    print('Selected voice: ' + voice)
    
    #Creating new record in Dynamo Db table 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME']) 
    table.put_item(
        Item={
        'id' : recordId, 
        'text' : text,
        'voice' : voice,
        'status' : 'PROCESSING'
        }
    )
    
    
    #Sending notification about new post to SNS 
    client = boto3.client('sns') 
    client.publish(
    TopicArn = os.environ['SNS_TOPIC'], Message = recordId
    )
    
    # Add CORS headers to the response
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps({'message': 'success', 'recordId': recordId}),
    }


    return response
