import recastai
from flask import jsonify
# RECAST.AI PART

RECAST_TOKEN = '1bce061fbb05eb4b99ca5588832cb9d7'
LANGUAGE = 'fr'

def analyse_text(sender,payload):
    request = recastai.Request(token=RECAST_TOKEN)
    response = request.analyse_text(payload)
    return response.raw

def converse(sender,payload):
    request = recastai.Request(token=RECAST_TOKEN)
    response = request.converse_text(payload)
    return response.raw

