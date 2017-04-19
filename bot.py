from wit import Wit
from flask import Flask,request, make_response
import logging
import requests
import json
import sys


# Definition des constantes
app = Flask(__name__)
WIT_ACCESS_TOKEN = '45O73DNGA4W6YBPS3GXJXAPTZK725XXE'

@app.route ('/webhook/', methods=['GET'])
def webhook_get():
    sys.stderr.write('Verify Token ' + request.args.get('hub.verify_token'))
    if request.args.get('hub.verify_token') == 'TOTO':
        return request.args.get('hub.challenge')
    else:
        return request.args.get('Error, Wrong Token')


@app.route('/webhook/', methods=['POST'])
def webhook_post():
    print(request.data[0].messaging)
    messaging_events = request.data[0].messaging
    for i in messaging_events :
        event = request.data[0].messaging[i]
        sender = event.sender.id
        if event.message and event.message.text:
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

FB_TOKEN = 'EAAD7Jwopoh4BAO6j1yJmn7ZAS3ikq6qQCgd5QqygxLlkO0LSEYPX9V3jSZADYIpJJPdNM6Ketmmgpg9U9MmVXbzWNk9sSf1W5ywKzSFVVplf1xouk9014HU7iDYEbK21mYmAa2pZC7kMxQzKu7ZBXxk73G2wIeTpamk4B5UPZBQZDZD'
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