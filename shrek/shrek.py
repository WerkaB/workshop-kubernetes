from flask import Flask
import json
import os
import random

app = Flask(__name__)

quotes_path = os.getenv("QUOTES_PATH",r"./")

quotes_filename = "quotes.json"
quotes = {}

with open(os.path.join(quotes_path, quotes_filename), "r", encoding="utf8") as file:    
    quotes = json.load(file)

@app.route("/shrek")
def shrek():
    shrek_quote = random.choice(quotes["Shrek"])
    print(shrek_quote)
    return shrek_quote

@app.route("/donkey")
def donkey():
    donkey_quote = random.choice(quotes["Donkey"])
    print(donkey_quote)
    return donkey_quote

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")