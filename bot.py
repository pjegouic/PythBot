#from wit import Wit
from flask import Flask,request, make_response
import logging
import requests
import json
import sys, os


# Definition des constantes
app = Flask(__name__)
WIT_ACCESS_TOKEN = '45O73DNGA4W6YBPS3GXJXAPTZK725XXE'

@app.route ('/webhooks/', methods=['GET'])
def webhook_get():
    if request.args.get('hub.verify_token') == 'TOTO':
        return request.args.get('hub.challenge')
    else:
        return 'Error, Wrong Token'


@app.route('/webhooks', methods=['POST'])
def webhook_post():
    sys.stderr.write(request.data)
    req = json.loads(request.data)
    reqType = type(req['entry')])
    reqContent = str(req['entry')])
    sys.stderr.write(str(reqType))
    sys.stderr.write(str(reqContent))
    messaging_events = req['entry'][0].messaging
    for i in messaging_events :
        event = req['entry'][0].messaging[i]
        sender = event.sender.id
        if event.message and event.message.text:
            text = event.message.text
            if text == 'Generic' :
                sys.stderr.write('Welcome to PythBot')
                continue
            sendTextMessage(sender, "Text received, echo : " + text)
        if event.postback :
            text = json.loads(event.postback)
            sendTextMessage(sender, "Text received, echo : " + text, FB_TOKEN)
            continue
    return 200


#FACEBOOK PART

FB_TOKEN = 'EAAD7Jwopoh4BAJ20sPZCt9ZC2Pl7ZCQmZAcVjRKBGs26g4v8uS26hymdknQwv4PBQOjn8ZAKX93lCVpuWulMnmzMtUdhn3puUpnT0iCZCra3H8RgBdN7UZBvBcE7jtPurDn9tsPvkH93I3aM3MWyXRA08IR6imLm48QHhanAB3PhwZDZD'
fb_url = 'https://graph.facebook.com/v2.6/me/messages'


def sendTextMessage(sender, text):
    messageData = {'text':text}
    header = {'Authorization' : 'access_token ' + FB_TOKEN}
    json = {'recipient' : {'id':sender}, 'message': messageData}
    try:
        response = requests.post(fb_url, header=header, json=json)
    except requests.exceptions.RequestException as e:
        logging.error('Error sending message : ' + e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'])


#client = Wit(access_token=WIT_ACCESS_TOKEN, actions=actions)