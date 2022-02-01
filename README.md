# Challenge

Tech Stack:

* Python 3
* AWS Serverless Application Model (SAM)
* AWS Cloudformation


In the SAM template, all AWS infrastructure elements are defined (IAM permissions, S3 bucket, Lambda function, dynamodb table). 

All 's3:ObjectCreated:*' are going to trigger the lambda which will stream the uploaded element into dynamodb


Some constraints:

The csvloader will load into a dynamo db table with the constraint of having at least one of the headers the field: 'uuid'. The load is done by 1000 elements batches and the test file (testfile.csv) with 100K rows was uploaded in about 2 min. 



