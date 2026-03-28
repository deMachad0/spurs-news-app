# Importing Flask and the tools we need to build the web and app
from flask import Flask, jsonify, render_template, send_from_directory
# Requests library allows us to make HTTP calls to external APIs
import requests
# CORS allows our app to communicate with other domains (avoids browser blocking)
from flask_cors import CORS 


from dotenv import load_dotenv
import os

API_KEY = os.getenv('API_KEY')
API_KEY2 = os.getenv('API_KEY2')

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
        matches = data.get('matches', [])
        # Filter only finished matches and get the last 4
        finished = [m for m in matches if m['status'] == 'FINISHED']
        return finished[-4:]
    # If something goes wrong, return None so we can handle the error elsewhere
    else:
        return None
    
# This function is responsible for fetching Spurs news data from the API
def fetch_spurs_news():
    
    # Building the URL to request Spurs news specifically
    url = f"https://newsapi.org/v2/everything"
    params = {
        'q': 'Tottenham Hotspurs',
        'language':'en',
        'sortBy':'publishedAt',
        'pageSize': 10,
        'apiKey': API_KEY2
    }
    response = requests.get(url, params=params)
    # If the request is successful (status 200), return the data as JSON
    if response.status_code == 200:
        data = response.json()
        return data.get('articles', [])
    # If something goes wrong, return None so we can handle the error elsewhere
    else:
        return None

# This function is reponsible for fetching Premier League Table from the API
def fetch_premier_league():

    #Building the URL to request PL table
    url = f"https://api.football-data.org/v4/competitions/PL/matches"
    headers = {"X-Auth-Token": API_KEY}
    params = {
        "status": "SCHEDULED"
    }
    response = requests.get(url, headers=headers, params=params)
    # If the request is successful (status 200), return the data as JSON
    if response.status_code == 200:
        data = response.json()
        matches = data.get('matches', [])
        return matches[:10]
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
    # Passing data to HTML template
    matches = fetch_news() or []
    articles = fetch_spurs_news() or []
    premier_league = fetch_premier_league() or []
    return render_template('spurs_news.html', matches=matches, articles=articles, premier_league=premier_league)

# This route loads the homepage into App
@app.route('/static/service_worker.js')
# Flask looks for service_worker.js inside the /static folder
def service_worker():
    return send_from_directory('static', 'service_worker.js')

# This ensures the app only runs when we execute this file directly
# debug=True allows us to see errors in the browser and auto-restarts on changes
if __name__ == "__main__":
    # Host='0.0.0.0' to Render access it
    app.run(host='0.0.0.0', port=5000, debug=False)