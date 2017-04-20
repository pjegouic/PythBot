#from wit import Wit
from flask import Flask,request, make_response
import logging
import requests
import json
import sys, os


# Definition des constantes
app = Flask(__name__)
WIT_ACCESS_TOKEN = '45O73DNGA4W6YBPS3GXJXAPTZK725XXE'
HTTP_OK = 200

@app.route ('/webhooks/', methods=['GET'])
def webhook_get():
    if request.args.get('hub.verify_token') == 'TOTO':
        return request.args.get('hub.challenge')
    else:
        return 'Error, Wrong Token'


@app.route('/webhooks', methods=['POST'])
def webhook_post():
    req = json.loads(request.data)
    response = make_response()
    messaging_events = req['entry'][0]['messaging']
    for i in range(len(messaging_events)):
        event = req['entry'][0]['messaging'][i]
        sys.stdout.write(str(event))
        sender = event['sender']['id']
        if 'message' in event and 'text' in event['message']:
            text = event['message']['text']
            sendTextMessage(sender, "En cours de développement. \n echo event.text : " + text)
        if 'postback' in event :
            text = json.loads(event.postback)
            sendTextMessage(sender, "En cours de développement. \n echo event.text : " + text, FB_TOKEN)
            continue
    return json.dumps(None,200,{'ContentType' : 'application/json'})



#FACEBOOK PART

FB_TOKEN = 'EAAD7Jwopoh4BAJ20sPZCt9ZC2Pl7ZCQmZAcVjRKBGs26g4v8uS26hymdknQwv4PBQOjn8ZAKX93lCVpuWulMnmzMtUdhn3puUpnT0iCZCra3H8RgBdN7UZBvBcE7jtPurDn9tsPvkH93I3aM3MWyXRA08IR6imLm48QHhanAB3PhwZDZD'
fb_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + FB_TOKEN


def sendTextMessage(sender, text):
    messageData = {'text':text}
    header = {'ContentType' : 'application/json'}
    json = {'recipient' : {'id':sender}, 'message': messageData}
    try:
        response = requests.post(fb_url, headers=header, json=json)
        sys.stdout.write(str(response.text))
    except requests.exceptions.RequestException as e:
        logging.error('Error sending message : ' + e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'])


#client = Wit(access_token=WIT_ACCESS_TOKEN, actions=actions)


