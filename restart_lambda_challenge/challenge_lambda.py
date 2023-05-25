import json
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')


def lambda_handler(event, context):
    """
    Check if uploaded to s3 bucket file has an extension ('txt', 'doc', 'docx').
    Count the number of words in the file.
    """
    topic_arn = 'arn:aws:sns:us-west-2:*********:testsns'

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    if file_key.split('.')[-1] in ['txt', 'doc', 'docx']:
        file_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = file_obj['Body'].read().decode('utf-8').strip().lstrip("\ufeff")
        sns.publish(
            TopicArn=topic_arn,
            Subject='Word Count Result',
            Message=f'The word count in the file {file_key} is {len(file_content.split())}'
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Sale Analysis Report sent.')
    }
