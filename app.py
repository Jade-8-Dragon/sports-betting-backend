from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes on your app

API_KEY = os.getenv("CFB_API_KEY")

@app.route("/")
def home():
    return {"message": "Backend is running!"}

@app.route("/api/games")
def get_games():

    selected_week = request.args.get('week', default=1, type=int)

    url = "https://api.collegefootballdata.com/games"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"year": 2025, "week": 7, "seasonType": "regular", "home": "Colorado"}

    response = requests.get(url, headers=headers, params=params)
    
    # Add error handling (good practice)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
        
    return jsonify(response.json())

# add other API call functions here:




if __name__ == "__main__":
    app.run(debug=True)