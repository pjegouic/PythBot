import recastai
from flask import jsonify
import requests
import httplib, urllib, base64
from itertools import izip

# RECAST.AI PART

RECAST_TOKEN = 'cfb4bbd5e7c87e8a7c12a07d28f4a797'
LANGUAGE = 'fr'

def analyse_text(sender,payload):
    request = recastai.Request(token=RECAST_TOKEN)
    response = request.analyse_text(payload)
    return response.raw

def converse(sender,payload):
    request = recastai.Request(token=RECAST_TOKEN)
    response = request.converse_text(payload)
    return response.raw

def bot(payload):
    connect = recastai.Connect(token=RECAST_TOKEN, language='fr')
    request = recastai.Request(token=RECAST_TOKEN)
    message = connect.parse_message(payload)
    response = request.converse_text(message.content, conversation_token=message.sender_id)
    # TRAITEMENT SEARCH_IMAGE WHEN IMAGE_CATEGORY FOUND
    if str(response.action.slug) == 'search_image' and response.action.done is True :
        reply_text = [{'type': 'text', 'content': response.action.reply}]        
        reply_image = [{'type': 'picture', 'content': 'https://imgflip.com/s/meme/Troll-Face.jpg'}]
        connect.send_message(reply_text, message.conversation_id)
        connect.send_message(reply_image, message.conversation_id)
        image_category = extract_memory(response.memory,"image_category")
        images = retrieve_image(image_category)
    else : 
        print ('RECAST RESPONSE : ' + response.raw.encode('utf-8'))
        content = 'SLUG : ' + response.action.slug + '\n' + 'DONE : ' + str(response.action.done) + '\n' + 'BOTREPLY : ' + response.action.reply
        replies = [{'type': 'text', 'content': content}]
        print('Conversation.id : ' + message.conversation_id)
        connect.send_message(replies, message.conversation_id)
    return jsonify(status=201)


def retrieve_image(category):
    headers = {
    # Request headers
    'Content-Type': 'multipart/form-data',
    'Ocp-Apim-Subscription-Key': '1581c54df3aa43d08c2aab6bf027d799',
    }
    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("POST", "/bing/v5.0/images/search?q=" + str(category), "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        data = dict(data)
        print data.value
        return data['value'][0]['thumbnailUrl']

    except Exception as e:
        print e


def extract_memory(memory, target):
    for item in memory :
        item = str(item)
        if item.find(target) != -1 :
            start = item.find("value=") + len("value=")
            end = len(item) - 1
            return item[start:end]
        else:
            return None


    