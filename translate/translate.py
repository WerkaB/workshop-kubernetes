from flask import Flask
import requests
import os

translate_fun = os.getenv("FUN", 'False').lower() in ('true', '1', 't', 'True')
shrek_service_url = os.getenv("SHREK_SERVICE_URL","http://0.0.0.0:5000")

translate_api_url_fun = "https://api.funtranslations.com/translate/doge.json"
translate_api_url_ru = "https://libretranslate.com/translate"

print(translate_fun)

app = Flask(__name__)

@app.route("/translate-shrek")
def translate_shrek():
    shrek_quote = requests.get(f"{shrek_service_url}/shrek")
    if translate_fun == True:
        response = translate_to_fun(shrek_quote)
    else:
        response = translate_to_ru(shrek_quote)
    return response

@app.route("/translate-donkey")
def translate_donkey():
    donkey_quote = requests.get(f"{shrek_service_url}/donkey")

    if translate_fun == True:
        response = translate_to_fun(donkey_quote)
    else:
        response = translate_to_ru(donkey_quote)
    return response

def translate_to_fun(quote_text: str):
    to_translate = f"text={quote_text}"
    translated = requests.post(translate_api_url_fun, data=to_translate, headers={"X-Funtranslations-Api-Secret": "<api_key>"})
    print(translated)
    return translated

def translate_to_ru(quote_text: str):
    to_translate = {
        "q": quote_text,
        "source": "auto",
        "target": "ru",
        "format": "text",
        "api_key": ""
	}
    translated = requests.post(translate_api_url_ru, data=to_translate, headers={"Content-Type": "application/json"})
    print(translated)
    return translated

if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")