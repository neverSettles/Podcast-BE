import openai
import os

from flask import Flask, jsonify, request
from dotenv import load_dotenv


# Set up OpenAI API credentials
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Call /generate to generate a podcast!"})

@app.route('/generate', methods=['POST'])
def create_post():
    data = request.get_json()  # parse parameters from incoming request

    topic = data.get('topic')  # get parameter called 'topic'
    duration = data.get('duration')  # get parameter called 'duration'
    tone = data.get('tone')  # get parameter called 'tone'

    # Call OpenAI API to generate podcast transcript
    prompt = f"Topic: {topic}\nDuration: {duration}\nTone: {tone}\n\nTranscript:\n"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    transcript = response.choices[0].text.strip()

    return jsonify({'message': transcript}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5001))
