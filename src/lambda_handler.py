import boto3
import os

transcribe = boto3.client('transcribe')
comprehend = boto3.client('comprehend')
rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    # 1. Process call recording
    call_recording = event['call_recording']
    
    # 2. Convert speech to text using Amazon Transcribe
    job_name = "call-transcription-job"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': call_recording},
        MediaFormat='wav',
        LanguageCode='en-US'
    )
    
    # 3. Analyze text with Amazon Comprehend
    text = "Sample text from call"  # Replace with transcribed text
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')['Sentiment']
    entities = comprehend.detect_entities(Text=text, LanguageCode='en')['Entities']
    
    # 4. Detect fraud keywords (example)
    fraud_keywords = ["urgent", "money", "danger", "help"]
    is_fraud = any(keyword in text.lower() for keyword in fraud_keywords)
    
    return {
        'statusCode': 200,
        'body': {
            'text': text,
            'sentiment': sentiment,
            'is_fraud': is_fraud
        }
    }
