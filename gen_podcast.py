import openai
import boto3
import os
import pyaudio
import io
import time
import argparse
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

parser = argparse.ArgumentParser(description='Podcast Generator')
parser.add_argument('-t', '--topic', help='Topic of the podcast')
parser.add_argument('-d', '--duration', help='Duration of the podcast in minutes')
args = parser.parse_args()

# def call_openai_api(prompt):
#     message=[{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages = message,
#         temperature=0.2,
#         max_tokens=1000,
#         frequency_penalty=0.0
#     )

#     return response.choices[0].text.strip()


def call_openai_api(prompt):
    # Define the parameters for the completion
    params = {
        'model': 'text-davinci-003',  # The model you want to use
        'prompt': prompt,
        'max_tokens': 3000,
        'temperature': 0.7,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }

    # Call the OpenAI API
    response = openai.Completion.create(**params)

    # Retrieve the generated text from the API response
    generated_text = response.choices[0].text.strip()

    return generated_text


def synthesize_speech(text):
    # Create a client using your AWS access keys stored as environment variables
    polly_client = boto3.Session(
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                    region_name=os.getenv('AWS_REGION', 'us-east-1')).client('polly')

    response = polly_client.synthesize_speech(VoiceId='Matthew',
                OutputFormat='mp3', 
                Text = text)

    # The response body contains the audio stream.
    # Writing the stream in a mp3 file
    filename = 'speech.mp3'
    with open(filename, 'wb') as file:
        file.write(response['AudioStream'].read())
    
    print("Speech synthesis completed. The output is stored as speech.mp3")

    # Play the audio file using pyaudio
    p = pyaudio.PyAudio()
    chunk = 1024
    stream = p.open(format=p.get_format_from_width(2), channels=1, rate=22050, output=True)
    audio_data = io.BytesIO(response['AudioStream'].read())
    data = audio_data.read(chunk)

    while data:
        stream.write(data)
        data = audio_data.read(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()



def create_podcast_prompt(topic, duration):
    # Create the podcast prompt
    meta_prompt = f"""
Please help me to make a prompt to GPT-3 to generate a podcast about {topic}.
The prompt should instruct GPT that the podcast should be {duration} minutes long.
The prompt should instruct GPT to make the podcast seem like a fluid conversation, without breaks in the conversation.
The prompt should instruct GPT that the text of the response should be the transcript of the podcast.
There should be no seperator between the segments, so that the podcast is one continuous audio file.
Please only output a prompt that I can use to send to GPT.
"""
    return meta_prompt


topic = args.topic
duration = args.duration
# topic = "Finding a girlfriend in the bay area as an Indian Software Engineer"
# duration = 10

meta_prompt = create_podcast_prompt(topic, duration)
print(meta_prompt)
time.sleep(5)  # Sleep for 5 seconds

prompt = call_openai_api(meta_prompt)
print(prompt)

story = call_openai_api(prompt)

print("Here is the story:")
print(story)

synthesize_speech(story)
