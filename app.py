from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("CFB_API_KEY")

@app.route("/")
def home():
    return {"message": "Backend is running!"}

@app.route("/api/games")
def get_games():
    url = "https://api.collegefootballdata.com/games"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"year": 2023, "week": 1, "seasonType": "regular"}

    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
