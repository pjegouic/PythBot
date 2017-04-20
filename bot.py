import recastai

# RECAST.AI PART

RECAST_TOKEN = '1bce061fbb05eb4b99ca5588832cb9d7'
LANGUAGE = 'fr'

def analyse_text(sender,payload):
    request = recastai.Request(token=RECAST_TOKEN)
    response = request.analyse_text(payload)
    return "TEXT INPUT SOURCE : " + str(response.source) + "\n" + "RESULTAT ANALYSE RECAST" +str(response.intents)

def converse(sender,payload):
    request = recastai.Request(token=RECAST_TOKEN)
    response = request.converse_text(payload)
    return "TEXT INPUT SOURCE : " + str(response.source) + "\n" + "RESULTAT ANALYSE RECAST" +str(response.intents)

