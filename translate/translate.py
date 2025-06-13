from flask import Flask
import requests
import os
import logging
import urllib.parse
import json

log = logging.getLogger("translate")
logging.basicConfig(level=10, format='%(asctime)s %(levelname)s: %(message)s')

translate_fun = os.getenv("FUN", 'False').lower() in ('true', '1', 't', 'True')
shrek_service_url = os.getenv("SHREK_SERVICE_URL","http://0.0.0.0:5000")

translate_api_url_fun = "https://api.funtranslations.com/translate/minion.json"
# translate_api_url_ru = "https://libretranslate.com/translate"
translate_api_url_ru = "https://api.funtranslations.com/translate/morse.json"

print(translate_fun)

app = Flask(__name__)

@app.route("/translate-shrek")
def translate_shrek():
    shrek_quote_response = requests.get(f"{shrek_service_url}/shrek")
    shrek_quote = shrek_quote_response.text
    log.info(f"shrek Quote from server: {shrek_quote}")
    print(shrek_quote)
    if translate_fun == True:
        response = translate_to_fun(shrek_quote)
    else:
        response = translate_to_ru(shrek_quote)
    return response

@app.route("/translate-donkey")
def translate_donkey():
    donkey_quote_response = requests.get(f"{shrek_service_url}/donkey")
    donkey_quote = donkey_quote_response.text
    log.info(f"Donkey Quote from server: {donkey_quote}")
    if translate_fun == True:
        response = translate_to_fun(donkey_quote)
    else:
        response = translate_to_ru(donkey_quote)
    return response

def translate_to_fun(quote_text: str):
    to_translate = f"text={urllib.parse.quote(quote_text, safe='')}"
    translated_response = requests.post(translate_api_url_fun, params=to_translate, headers={"Content-Type": "application/x-www-form-urlencoded", "X-Funtranslations-Api-Secret": "<api_key>"})
    translated = translated_response.content
    log.info(f"translated: {translated}")
    return translated

# def translate_to_ru(quote_text: str):
#     to_translate = json.dumps({
#         "q": urllib.parse.quote(quote_text, safe=''),
#         "source": "auto",
#         "target": "pl",
#         "format": "text",
#         "api_key": ""
# 	})
#     translated_response = requests.post(translate_api_url_ru, data=to_translate, headers={"Content-Type": "application/json"})
#     translated = translated_response.content
#     log.info(f"translated: {translated}")
#     return translated

def translate_to_ru(quote_text: str):
    to_translate = f"text={urllib.parse.quote(quote_text, safe='')}"
    translated_response = requests.post(translate_api_url_fun, params=to_translate, headers={"Content-Type": "application/x-www-form-urlencoded", "X-Funtranslations-Api-Secret": "<api_key>"})
    translated = translated_response.content
    log.info(f"translated: {translated}")
    return translated

if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")