# Develop-a-text-narrator-using-Amazon-Polly

3.1 Project Overview
In this project, we will develop a text narrator using Amazon Polly, a cloud service that converts text into lifelike speech. We will create an IAM role, an S3 bucket, and a Lambda function to orchestrate the text-to-speech process. The final output will be an audio file stored in the S3 bucket.

3.2 Getting Started with Amazon Polly
Amazon Polly is a service that turns text into lifelike speech, allowing applications to "speak" in various voices and languages. To use Amazon Polly, you need an AWS account and the AWS CLI installed and configured.

Prerequisites:
An AWS account
AWS CLI installed and configured
Basic knowledge of AWS services like IAM, S3, and Lambda

3.3 Steps
3.3A Create an IAM Role
Sign in to the AWS Management Console.
Navigate to the IAM service.
Create a new role:
Select Lambda as the trusted entity.
Attach the following policies:
AmazonPollyFullAccess
AmazonS3FullAccess
Name the role PollyLambdaRole.

3.3B Create an S3 Bucket
Navigate to the S3 service in the AWS Management Console.
Create a new bucket:
Name the bucket (e.g., text-narrator-bucket).
Select the region.
Adjust the settings as needed (e.g., enabling versioning or encryption).

3.3C Create a Lambda Function
Navigate to the Lambda service in the AWS Management Console.
Create a new function:
Select Author from scratch.
Name the function (e.g., TextToSpeechFunction).
Choose Python 3.x as the runtime.
Select the previously created PollyLambdaRole for the execution role.
Add code to the Lambda function:
Use the following Python code to convert text to speech and save the output in the S3 bucket:

python:

import boto3
import os

def lambda_handler(event, context):
    # Initialize Polly and S3 clients
    polly = boto3.client('polly')
    s3 = boto3.client('s3')
    
    # Define the text to convert
    text = event.get('text', 'Hello, this is a test message from Amazon Polly.')
    
    # Define the output file
    output_format = 'mp3'
    bucket_name = 'text-narrator-bucket'
    object_name = 'output.mp3'
    
    # Convert text to speech
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId='Joanna'
    )
    
    # Save the audio stream to a file in S3
    if "AudioStream" in response:
        with open('/tmp/output.mp3', 'wb') as file:
            file.write(response['AudioStream'].read())
        s3.upload_file('/tmp/output.mp3', bucket_name, object_name)
    
    return {
        'statusCode': 200,
        'body': f"Text has been converted to speech and saved to s3://{bucket_name}/{object_name}"
    }
    
Deploy the function:
Save the changes and deploy the function.

3.3D Check the Output
1. Invoke the Lambda Function Manually or Through an Event Trigger
Manual Invocation:

Go to the AWS Lambda console.
Select your function (TextToSpeechFunction).
Click on the Test button to create a new test event.
Configure a new test event by giving it a name and providing a JSON payload. For example:
json

{
    "text": "Hello, this is a test message from Amazon Polly."
}

Click on Create and then Test again to invoke the function manually.
Event Trigger:

Alternatively, you can set up an event trigger such as an S3 event, API Gateway, or CloudWatch Events to invoke your Lambda function. For example, you can set up an API Gateway to trigger the function when an HTTP request is made.

2. Check the S3 Bucket (text-narrator-bucket) for the output.mp3 File
Navigate to the S3 service in the AWS Management Console.
Open your S3 bucket (e.g., text-narrator-bucket).
Look for the output.mp3 file in the bucket. This file should have been created and uploaded by your Lambda function.

3. Download and Play the Audio File to Verify the Text-to-Speech Conversion
Select the output.mp3 file in the S3 bucket.
Click on the Download button to download the file to your local machine.
Open the downloaded output.mp3 file using any media player that supports MP3 playback (e.g., VLC Media Player, Windows Media Player).
Listen to the audio file to verify that the text was correctly converted to speech by Amazon Polly.

3.4 Conclusion & Clean-up
In this project, we successfully created a text narrator using Amazon Polly. We set up the necessary AWS resources, including an IAM role, an S3 bucket, and a Lambda function. Finally, we verified the output by checking the audio file in the S3 bucket.

Clean-up:
Delete the Lambda function: Navigate to the Lambda service and delete the TextToSpeechFunction.
Delete the S3 bucket: Navigate to the S3 service, empty the text-narrator-bucket, and delete it.
Delete the IAM role: Navigate to the IAM service and delete the PollyLambdaRole.



