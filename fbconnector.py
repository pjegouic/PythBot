from flask import Flask,request, make_response
import logging
import requests
import json
import sys, os

class fbconnector:
    def __init__(self):
        self.FB_TOKEN = 'EAAD7Jwopoh4BAJ20sPZCt9ZC2Pl7ZCQmZAcVjRKBGs26g4v8uS26hymdknQwv4PBQOjn8ZAKX93lCVpuWulMnmzMtUdhn3puUpnT0iCZCra3H8RgBdN7UZBvBcE7jtPurDn9tsPvkH93I3aM3MWyXRA08IR6imLm48QHhanAB3PhwZDZD'
        self.fb_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + self.FB_TOKEN
        self.HEADER = {'ContentType' : 'application/json'}

    def prepare_response(self,recipient_id, message):
        payload = {
            'recipient' : {'id' : recipient_id}
            }
        message = {
            'text' : message
        }
        payload.message = message
        return payload

    def parse_from_facebook(self,body):
        return json.loads(body)

    def send(self,json):
        try:
            response = requests.post(self.fb_url, headers=self.HEADER, json=json)
            sys.stdout.write(str(response.text))
        except requests.exceptions.RequestException as e:
            sys.stderr.write(('Error sending message : ' + e))

    def sendRichTextMessage(self,sender):
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
            response = requests.post(self.fb_url, headers=self.HEADER, json=json)
        except requests.HTTPError as e:
            sys.stderr.write(('Error sending message : ' + e))
            sys.stderr.close