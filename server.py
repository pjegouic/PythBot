from flask import Flask,request, make_response
import logging
import requests
import json
import sys, os
import recastai
from bot import bot
import fbconnector


# Definition des constantes
app = Flask(__name__)


@app.route ('/webhooks/', methods=['GET'])
def webhook_get():
    if request.args.get('hub.verify_token') == 'TOTO':
        return request.args.get('hub.challenge')
    else:
        return 'Error, Wrong Token'


@app.route('/webhooks', methods=['POST'])
def webhook_post():
    req = fbconnector.parse_from_facebook(request.data)
    messaging_events = req['entry'][0]['messaging']
    for i in range(len(messaging_events)):
        event = req['entry'][0]['messaging'][i]
        sys.stdout.write(str(event))
        sys.stdout.close
        sender = event['sender']['id']
        if 'message' in event and 'text' in event['message']:
            text = event['message']['text']
            bot_response = bot.converse(sender,text)
            fbconnector.send(fbconnector.prepare_response(sender,bot_response))
        if 'postback' in event :
            text = event['postback']['payload']
            #bot.sendsendSimpleTextMessage(sender, "En cours de developpement. echo event.text : " + text)
            continue
    return json.dumps(None,200,{'ContentType' : 'application/json'})

@app.route('/', methods=['POST'])
def recast_connector():
    return bot(request)


if __name__ == '__main__':
    #port = os.environ['PORT']
    port = 5000
    app.run(host='0.0.0.0', port=port)