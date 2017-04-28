import recastai
from flask import jsonify
import json
import requests
import httplib, urllib, base64
from itertools import izip
from random import randint
import searchimage

# RECAST.AI PART

RECAST_TOKEN = 'cfb4bbd5e7c87e8a7c12a07d28f4a797'
LANGUAGE = 'fr'

class PythBot:
    def __init__(self):
        self.request = recastai.Request(token=RECAST_TOKEN, language='fr')

    def analyse_text(self,sender,payload):
        return self.request.analyse_text(payload).raw

    def converse(self,sender,payload):
        return self.request.converse_text(payload)

    def brain(self, senderid, query):
        # Envoi du message a Recast.ai pour analyse
        response = self.request.converse_text(query, conversation_token=senderid)
        resp = []
        ###############################################
        # PythBot Brain - Traitement retour Recast.ai #
        ###############################################
        if response.action.slug and response.action.reply:
            #########################
            # Intent : search_image #
            #########################
            if str(response.action.slug) == 'greetings':
                reply_text = [{'type': 'text', 'content': None}]
                reply_text[0]['content'] = response.action.reply
                resp.insert(0,reply_text)
            elif str(response.action.slug) == 'search_image':
                ###############
                # Intent Done #
                ###############
                if  response.action.done is True :
                    # Preparation du contenu de la reponse textuelle
                    reply_text = [{'type': 'text', 'content': None}]
                    reply_text[0]['content'] = response.action.reply
                    resp.insert(0,reply_text)
                    # Preparation recherche image
                    image_category = self.extract_memory(response.memory,"image_category")
                    images_response = searchimage.retrieve_image(image_category)
                    i = 1
                    for item in images_response:
                        reply_image = [{'type': 'picture', 'content': None}]
                        reply_image[0]['content'] = item
                        resp.insert(i,reply_image)
                        i = i +1  
                #############
                # Continue  #
                #############
                else : 
                    # Preparation contenu de la reponse textuelle
                    reply_text = [{'type': 'text', 'content': None}]
                    reply_text[0]['content'] = response.action.reply
                    resp.insert(0,reply_text)
            ##################
            # Intent : order #
            ##################
            elif str(response.action.slug) == 'order':
                ###############
                # Intent Done #
                ###############
                if  response.action.done is True :
                    # Preparation du contenu de la reponse textuelle
                    reply_text = [{'type': 'text', 'content': None}]
                    reply_text[0]['content'] = response.action.reply
                    resp.insert(0,reply_text)
                #############
                # Continue  #
                #############
                else : 
                    # Preparation contenu de la reponse textuelle
                    reply_text = [{'type': 'text', 'content': None}]
                    reply_text[0]['content'] = response.action.reply
                    resp.insert(0,reply_text)
        else:
                print 'RECAST RESPONSE : '
                print response.raw
                reply_text = [{'type': 'text', 'content': None}]
                reply_text[0]['content'] = response.action.reply
                resp.insert(0,reply_text)
        return resp

    def extract_memory(self, memory, target):
        for item in memory :
            item = str(item)
            if item.find(target) != -1 :
                start = item.find("value=") + len("value=")
                end = len(item) - 1
                return item[start:end]
            else:
                return None


    
