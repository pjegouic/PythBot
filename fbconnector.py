from flask import Flask,request, make_response
import logging
import requests
import recastai
import json
from bot import PythBot
import sys, os

FB_TOKEN = 'EAAD7Jwopoh4BAJcCi5IGh0eqBRkvZBcCds2MF6ONiwHPFFBZAY7nqHCKd5DR7PEUX1kNKmNUGix9qLHVjDa3QZAGZCoymt0oWRhz1xe4rRSIZAwJf3HmgiUASCr4MBt5zZBZA3gjGXwrcwahuHWwiZCsQwjtviLwOKU65MyFKKtxlQZDZD'
fb_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + FB_TOKEN
HEADER = {'ContentType' : 'application/json'}
# Definition des constantes
# Definition des constantes
app = Flask(__name__)
RECAST_TOKEN = 'cfb4bbd5e7c87e8a7c12a07d28f4a797'
LANGUAGE = 'fr'
connect = recastai.Connect(token=RECAST_TOKEN, language='fr')

def sendMessage(sender,content):
    print "SIMPLE TEMPLATE CONTENT : "
    print content
    json = {
        'recipient': {'id': sender},
        'message': {'text': content[0]['content']}
        }
    try:
        response = requests.post(fb_url, headers=HEADER, json=json)
    except Exception as e:
        pass

# Format du content : [{ 'type' : string, 'content' : string}] #Content correspond a l'URL a afficher.
def sendWithGenericTemplate(sender, content):
    print "GENERIC TEMPLATE CONTENT : "
    print content
    resp_skeleton = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': []
                }
            }
        }
    i = 0
    for item in content :
        element = {
            'title' : 'TODO : REPLACE_TITLE',
            'image_url' : item[0]['content'] 
        }
        resp_skeleton['attachment']['payload']['elements'].insert(i, element)
        i = i+1
        
    json = {'recipient' : {'id':sender}, 'message': resp_skeleton}
    try:
        print 'SENDING RESPONSE'
        print json
        response = requests.post(fb_url, headers=HEADER, json=json)
        print response.text
    except Exception as e:
        print e

@app.route ('/webhooks', methods=['GET'])
def webhook_get():
    if request.args.get('hub.verify_token') == 'TOTO':
        return request.args.get('hub.challenge')
    else:
        return 'Error, Wrong Token'


@app.route('/webhooks', methods=['POST'])
def webhook_post():
    try:
        fb_input = fbconnector_request_adapter(request.data)
        if fb_input is not None:
            bot = PythBot()
            response = bot.brain(fb_input['sender'] , fb_input['query'])
            if len(response) > 1:
                print 'SUBLIST RESPONSE'
                print response[1:(len(response)-1)]
                sendMessage(fb_input['sender'], response[0])
                sendWithGenericTemplate(fb_input['sender'], response[1:(len(response))])
                return json.dumps(None,200,{'ContentType' : 'application/json'})
            elif len(response) == 1:
                print 'len == 1 condition'
                print response
                sendMessage(fb_input['sender'],response[0])
                return json.dumps(None,200,{'ContentType' : 'application/json'})
            else:
                return json.dumps(None,200,{'ContentType' : 'application/json'})
        else:
            return json.dumps(None,200,{'ContentType' : 'application/json'})
    except Exception as e:
        print 'STACK TRACE ERROR : ' + str(e)
        return json.dumps(None,200,{'ContentType' : 'application/json'})
    
    


def fbconnector_request_adapter(payload):
    request = json.loads(payload)
    mess_events = request['entry'][0]['messaging']
    for i in range(len(mess_events)):
        message = request['entry'][0]['messaging'][i]
        sender = message['sender']['id']
        if 'message' in message and 'text' in message['message']:
            return {'query' : message['message']['text'], 'sender' : sender}
        elif 'postback' in message :
            #Todo Postback Management
            return None
        else:
            return None

def fbconnector_response_adapter(payload):
    return None



if __name__ == '__main__':
    #port = os.environ['PORT']
    port = 8000
    app.run(host='0.0.0.0', port=port)