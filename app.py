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

    selected_year = request.args.get('year', default=2025, type=int)
    selected_week = request.args.get('week', type=int)
    home_team = request.args.get('home', type=str) # Mapped from 'homeTeam'

    # These are for sorting/limiting *after* we get the data
    limit = request.args.get('limit', type=int)
    sort_by = request.args.get('sort', type=str) # e.g., 'gameDate'
    order = request.args.get('order', default='desc', type=str) # 'asc' or 'desc'


    # 2. Build the parameters for the external API call
    url = "https://api.collegefootballdata.com/games"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Start with required params
    params = {
        "year": selected_year,
        "seasonType": "regular"
    }

    # Add optional params only if they were provided
    if selected_week:
        params["week"] = selected_week
        
    if home_team:
        params["home"] = home_team # 'homeTeam' from frontend becomes 'home' for the API

    response = requests.get(url, headers=headers, params=params)
    
    # Check if the external API call failed
    response.raise_for_status() 
    
    data = response.json()

    # 3. Perform sorting (if requested)
    # We sort the data here because the API doesn't do it for us.
    if sort_by == 'gameDate' and data:
        # Check if gameDate is available, default to empty string if not
        is_desc = (order == 'desc')
        data.sort(key=lambda game: game.get('start_date', ''), reverse=is_desc)

    # 4. Perform limiting (if requested)
    # We slice the list to get just the "N" items
    if limit and data:
        data = data[:limit] # Get the first N items (top N if sorted)

    # 5. Return the final, processed data
    return jsonify(data)

# add other API call functions here:




if __name__ == "__main__":
    app.run(debug=True)