import openai
import os

from generate import gen_podcast

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
    
    transcript = gen_podcast.create_podcast(topic, duration)

    return jsonify({'message': transcript}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5001))