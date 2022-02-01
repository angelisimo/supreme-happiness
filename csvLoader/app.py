import json
import csv
import boto3
import urllib.parse
import logging
import os
from smart_open import open
import codecs




logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
tableName = os.environ['table']



def lambda_handler(event,context):

    s3 = boto3.resource('s3')
    

    for record in event['Records']:
        bucketName = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus (record['s3']['object']['key'])
        uri = 's3://{}/{}'.format(bucketName, key)


        #with open(uri) as fin:
        #    header = fin.readline()
            
        #    for row in fin:
        #        writetodynamo(row)

        try:
            obj = s3.Object(bucketName, key).get()['Body']
        except:
            print("S3 Object could not be opened. Check environment variable."),

        batch_size = 1000
        batch = []
        

        for row in csv.DictReader(codecs.getreader('utf-8')(obj)):
            if len(batch) >= batch_size:
                writetodynamo(batch)
                batch.clear()
            batch.append(row)

        if batch:
            writetodynamo(batch)
    
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Uploaded to dynamo"}),
        "headers": {
            "Content-Type": "application/json"
        }}


def writetodynamo(rows):
    try:
        table = dynamodb.Table(tableName)
    except:
        print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")
    
    try:
        with table.batch_writer() as batch:
            for i in range(len(rows)):
                batch.put_item(Item=rows[i])
    except Exception as e:
        print("Error executing batch_writer")
        print (e)


    return True
