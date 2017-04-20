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
                sendSimpleTextMessage(sender, "En cours de développement. echo event.text : " + text)
        if 'postback' in event :
            text = json.loads(event.postback)
            sendSimpleTextMessage(sender, "En cours de développement. echo event.text : " + text)
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
					'title': 'First card',
				    'subtitle': 'Element #1 of an hscroll',
				    'image_url': 'http://messengerdemo.parseapp.com/img/rift.png',
				    'buttons': [{
					    'type': 'web_url',
					    'url': 'https://www.messenger.com',
					    'title': 'web url'
				    }, {
					    'type': 'postback',
					    'title': 'Postback',
					    'payload': 'Payload for first element in a generic bubble',
				    }],
			    }, {
				    'title': 'Second card',
				    'subtitle': 'Element #2 of an hscroll',
				    'image_url': 'http://messengerdemo.parseapp.com/img/gearvr.png',
				    'buttons': [{
					    'type': 'postback',
					    'title': 'Postback',
					    'payload': 'Payload for second element in a generic bubble',
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


