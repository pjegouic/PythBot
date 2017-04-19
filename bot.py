from wit import Wit
from flask import Flask, make_response
import logging
import requests
import json


# Definition des constantes
app = Flash(__name__)
WIT_ACCESS_TOKEN = '45O73DNGA4W6YBPS3GXJXAPTZK725XXE'

@app.route ('/webhook/', method=['GET'])
def webhook_get():
    if request.args.get('hub.verify_token') == 'TOTO':
        return request.args.get('hub.challenge')
    else:
        return request.args.get('Error, Wrong Token')


@app.route('/webhook/', method=['POST'])
def webhook_post():
    print(request.data[0].messaging)
    messaging_events = request.data[0].messaging
    for i in messaging_events :
        event = request.data[0].messaging[i]
        sender = event.sender.id
        if event.message and event.message.text
            text = event.message.text
            if text == 'Generic' :
                logging.info('Welcome to PythBot')
                #sendGenericMessage(sender)
                continue
            sendTextMessage(sender, "Text received, echo : " + text)
        if event.postback :
            text = json.loads(event.postback)
            sendTextMessage(sender, "Text received, echo : " + text, token)
            continue
    return 200


#FACEBOOK PART

FB_TOKEN = 'TOTOTO'
fb_url = 'https://graph.facebook.com/v2.6/me/messages'


def sendTextMessage(sender, text):
    messageData = {'text':text}
    header = {'Authorization' : 'access_token ' + FB_TOKEN}
    json = {'recipient' : {'id':sender}, 'message': messageData}
    try:
        response = requests.post(fb_url, header=header,json=json)
    except requests.exceptions.RequestException as e:
        logging.error('Error sending message : ' + e)

if __name__ == '__main__':
    app.run()

actions = {
    'send': send,
    'my_action': my_action,
}

client = Wit(access_token=WIT_ACCESS_TOKEN, actions=actions)