import boto3

def lambda_handler(event, context):
    polly = boto3.client('polly')
    s3 = boto3.client('s3')

    text = event.get('text', 'Hello, this is a test message from Amazon Polly.')
    output_format = 'mp3'
    bucket_name = 'text-narrator-bucket'
    object_name = 'output.mp3'

    response = polly.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId='Joanna'
    )

    if "AudioStream" in response:
        with open('/tmp/output.mp3', 'wb') as file:
            file.write(response['AudioStream'].read())
        s3.upload_file('/tmp/output.mp3', bucket_name, object_name)

    return {
        'statusCode': 200,
        'body': f"Text has been converted to speech and saved to s3://{bucket_name}/{object_name}"
    }
