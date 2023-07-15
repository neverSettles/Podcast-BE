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
    return jsonify({"Choo Choo": "Isaac is awesome"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5001))
