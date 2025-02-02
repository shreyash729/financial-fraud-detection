import boto3
import time
import json
import urllib.request

# Initialize AWS clients
transcribe = boto3.client('transcribe')
comprehend = boto3.client('comprehend')
rekognition = boto3.client('rekognition')

def start_transcription(call_recording):
    """Starts an Amazon Transcribe job and returns the job name."""
    job_name = f"call-transcription-{int(time.time())}"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': call_recording},
        MediaFormat='wav',
        LanguageCode='en-US'
    )
    return job_name

def get_transcription_result(job_name):
    """Waits for transcription to complete and retrieves the text."""
    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = response['TranscriptionJob']['TranscriptionJobStatus']

        if status == 'COMPLETED':
            transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            return extract_transcribed_text(transcript_uri)
        
        if status == 'FAILED':
            return None  

        time.sleep(5)  

def extract_transcribed_text(transcript_uri):
    """Downloads and extracts text from the transcription result."""
    response = urllib.request.urlopen(transcript_uri)
    transcript_data = json.loads(response.read())
    return transcript_data['results']['transcripts'][0]['transcript']

def analyze_text(text):
    """Analyzes text using Amazon Comprehend for sentiment and named entities."""
    sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = sentiment_response['Sentiment']

    entities_response = comprehend.detect_entities(Text=text, LanguageCode='en')
    entities = [entity['Text'] for entity in entities_response['Entities']]

    return sentiment, entities

def detect_fraud(text):
    """Detects fraud based on keywords and negative sentiment."""
    fraud_keywords = ["urgent", "money", "danger", "help", "account", "password", "transfer"]
    is_fraud = any(keyword in text.lower() for keyword in fraud_keywords)

    sentiment, _ = analyze_text(text)
    if sentiment == "NEGATIVE" or is_fraud:
        return True

    return False

def analyze_image(image_s3_bucket, image_s3_key):
    """Analyzes an image using Amazon Rekognition for text and emotions."""
    response = rekognition.detect_text(
        Image={'S3Object': {'Bucket': image_s3_bucket, 'Name': image_s3_key}}
    )
    
    detected_text = " ".join([item['DetectedText'] for item in response['TextDetections']])
    
    # Check if the image text contains fraud-related words
    fraud_detected = detect_fraud(detected_text)

    return detected_text, fraud_detected

def lambda_handler(event, context):
    try:
        # 1. Get call recording URL from the event
        call_recording = event['call_recording']

        # 2. Start Transcription
        job_name = start_transcription(call_recording)
        transcribed_text = get_transcription_result(job_name)

        if not transcribed_text:
            return {"statusCode": 500, "body": "Transcription failed."}

        # 3. Analyze Transcribed Text
        sentiment, entities = analyze_text(transcribed_text)
        is_fraud = detect_fraud(transcribed_text)

        # 4. Check for an Image (if provided)
        detected_image_text = None
        image_fraud_detected = False

        if "image_s3_bucket" in event and "image_s3_key" in event:
            detected_image_text, image_fraud_detected = analyze_image(
                event["image_s3_bucket"], event["image_s3_key"]
            )

        # 5. Combine Results
        final_fraud_status = is_fraud or image_fraud_detected

        return {
            'statusCode': 200,
            'body': {
                'text': transcribed_text,
                'sentiment': sentiment,
                'entities': entities,
                'is_fraud': final_fraud_status,
                'detected_image_text': detected_image_text
            }
        }

    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}
