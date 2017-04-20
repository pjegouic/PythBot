from flask import Flask,request, make_response
import logging
import requests
import json
import sys, os
import recastai


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
        sys.stdout.close
        sender = event['sender']['id']
        if 'message' in event and 'text' in event['message']:
            text = event['message']['text']
            if text == 'richtext':
                sendRichTextMessage(sender)
            elif text == 'recast':
                recast(text)
            else:
                sendSimpleTextMessage(sender, "En cours de developpement. echo event.text : " + text)
        if 'postback' in event :
            text = event['postback']['payload']
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


def sendRichTextMessage(sender, payload):
    messagedata = {
	    'attachment': {
		    'type': 'template',
		    'payload': {
				'template_type': 'generic',
			    'elements': [{
					'title': 'Une pomme',
				    'subtitle': 'Variete Golden',
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
        sys.stderr.close

# RECAST.AI PART

RECAST_TOKEN = '1bce061fbb05eb4b99ca5588832cb9d7'
LANGUAGE = 'fr'
PORT = '5000'

def recast(payload):
    connect = recastai.Connect(token=RECAST_TOKEN, language=LANGUAGE)
    request = recastai.Request(token=RECAST_TOKEN)

    message = payload
    response = request.converse_text(message, conversation_token = message.sender_id)
    sys.stdout.write(str(response))
    sys.stdout.close
    replies = [{'type' : 'text', 'content' : r} for r in response.replies]
    connect.send_message(replies,message.conversation_id)
    return json.dumps(None,200,{'ContentType' : 'application/json'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'])

