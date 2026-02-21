# Importing Flask and the tools we need to build the web app
from flask import Flask, jsonify, render_template
# Requests library allows us to make HTTP calls to external APIs
import requests
# CORS allows our app to communicate with other domains (avoids browser blocking)
from flask_cors import CORS 
# Importing the API key stored separately in config.py for security
from config import API_KEY

from dotenv import load_dotenv
import os

API_KEY = os.getenv('API_KEY')

# Creating the Flask application instance
app = Flask(__name__)
# Applying CORS to the entire app
CORS(app)

# This function is responsible for fetching Spurs match data from the API
def fetch_news():
    # Tottenham Hotspur's unique ID on the Football-Data.org API
    SPURS_ID = 73
    # Building the URL to request Spurs matches specifically
    url = f"https://api.football-data.org/v4/teams/{SPURS_ID}/matches"
    
    # The API requires authentication via this header using our API key
    headers = {"X-Auth-Token": API_KEY}

    # Making the GET request to the API
    response = requests.get(url, headers=headers)

    # If the request is successful (status 200), return the data as JSON
    if response.status_code == 200:
        data = response.json()
        return data
    # If something goes wrong, return None so we can handle the error elsewhere
    else:
        return None

# This route handles GET requests to /spurs and returns the match data as JSON    
@app.route('/spurs', methods=['GET'])
def get_spurs():
    # Calling fetch_news() to retrieve the data
    data = fetch_news()
     # If data was returned successfully, send it as a JSON response
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Could not fetch Spurs data'}), 500

# This route loads the homepage and renders our HTML template
@app.route('/')
# Flask looks for spurs_news.html inside the /templates folder
def index():
    return render_template('spurs_news.html')

# This ensures the app only runs when we execute this file directly
# debug=True allows us to see errors in the browser and auto-restarts on changes

if __name__ == "__main__":
    app.run(debug=True)