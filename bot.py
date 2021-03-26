from flask_sslify import SSLify
from flask import request
from flask import jsonify
from flask import Flask
import pandas as pd
import requests, json, time, csv

URL = 'https://api.telegram.org/botTOKEN'

app = Flask(__name__)
sslify = SSLify(app)

def get_code(code):
    codes = pd.read_csv('code.csv')
    try:
        result = codes.loc[codes['code'] == code, 'region'].values[0]
    except:
        result = "Неверно введён код региона"    
    return result

def send_message(chat_id, text='None!'):
    url = URL + 'sendMessage'
    answer = {'chat_id':chat_id, 'text':text}
    r = requests.post(url, json=answer)
    return r.json()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        text = get_code(int(message))
        send_message(chat_id, text=text)
        return jsonify(r)

    return '<h1>main page</h1>'

if __name__ == '__main__':
    app.run()