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
            if text == 'richtext' :
                sendRichTextMessage(sender)
            else:
                sendSimpleTextMessage(sender, "En cours de developpement. echo event.text : " + text)
        if 'postback' in event :
            sendSimpleTextMessage(sender, "En cours de developpement. echo event.text : " + text)
            continue
    return json.dumps(None,200,{'ContentType' : 'application/json'})



#FACEBOOK PART

FB_TOKEN = 'EAAD7Jwopoh4BAJ20sPZCt9ZC2Pl7ZCQmZAcVjRKBGs26g4v8uS26hymdknQwv4PBQOjn8ZAKX93lCVpuWulMnmzMtUdhn3puUpnT0iCZCra3H8RgBdN7UZBvBcE7jtPurDn9tsPvkH93I3aM3MWyXRA08IR6imLm48QHhanAB3PhwZDZD'
fb_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + FB_TOKEN
HEADER = {'ContentType' : 'application/json'}

def sendSimpleTextMessage(sender, text):
    messagedata = {'text':text}
    json = {'recipient' : {'id':sender}, 'message': messagedata}
    try:
        response = requests.post(fb_url, headers=HEADER, json=json)
        sys.stdout.write(str(response.text))
    except requests.exceptions.RequestException as e:
        sys.stderr.write(('Error sending message : ' + e))


def sendRichTextMessage(sender):
    messagedata = {
	    'attachment': {
		    'type': 'template',
		    'payload': {
				'template_type': 'generic',
			    'elements': [{
					'title': 'Une pomme',
				    'subtitle': 'Variété Golden',
				    'image_url': 'https://fridg-front.s3.amazonaws.com/media/products/pomme_golden.jpg',
				    'buttons': [{
					    'type': 'web_url',
					    'url': 'http://lescomptoirs.com',
					    'title': 'Les Comptoirs'
				    }, {
					    'type': 'postback',
					    'title': 'Postback',
					    'payload': 'Postback Apple payload',
				    }],
			    }, {
				    'title': 'Une banane',
				    'subtitle': 'Banana',
				    'image_url': 'https://www.topsante.com/var/topsante/storage/images/medecine/troubles-cardiovasculaires/avc/prevenir/avc-une-banane-par-jour-peut-reduire-le-risque-31817/207515-3-fre-FR/AVC-une-banane-par-jour-peut-reduire-le-risque.jpg',
				    'buttons': [{
					    'type': 'postback',
					    'title': 'Postback',
					    'payload': 'Postback Banana payload',
				    }],
			    }]
		    }
	    }
    }
    json = {'recipient' : {'id':sender}, 'message': messagedata}
    try:
        response = requests.post(fb_url, headers=HEADER, json=json)
    except requests.HTTPError as e:
        sys.stderr.write(('Error sending message : ' + e))




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'])


#client = Wit(access_token=WIT_ACCESS_TOKEN, actions=actions)


