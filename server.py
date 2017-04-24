from flask import Flask,request, jsonify
import logging
import requests
import json
import sys, os
import recastai
from bot import PythBot
import fbconnector


# Definition des constantes
app = Flask(__name__)
RECAST_TOKEN = 'cfb4bbd5e7c87e8a7c12a07d28f4a797'
LANGUAGE = 'fr'
connect = recastai.Connect(token=RECAST_TOKEN, language='fr')


# Structure de request attendu
# { 'message' : { 'data' : { 'username' : string }, participant, conversation }}
@app.route('/', methods=['POST'])
def recast_adapter():
    bot = PythBot()
    message = connect.parse_message(request)
    response = bot.brain(message.sender_id ,message.content)
    send(message.conversation_id, response)
    return jsonify(status=201)

def send(target,payload):
    print 'SENDING ...'
    print payload
    for item in payload:
        connect.send_message(item, target)
        
if __name__ == '__main__':
    #port = os.environ['PORT']
    port = 5000
    app.run(host='0.0.0.0', port=port)