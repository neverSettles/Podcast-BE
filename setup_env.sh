#!/bin/bash

# Creating virtual environment
python3 -m venv copilotenv

# Activating the environment
source copilotenv/bin/activate

# Check if requirements.txt file exists
if [ -f "requirements.txt" ]; then
    echo "requirements.txt found. Installing requirements."
    pip3 install -r requirements.txt
else
    echo "No requirements.txt file found."
fi
