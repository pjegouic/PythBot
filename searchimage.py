import httplib, urllib, base64, json
from random import randint

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
            images = json.loads(data)
            conn.close()
            random_index = randint(0,len(images['value'])-1)
            response = []
            response.insert(0, images['value'][(randint(0,len(images['value'])-1))]['thumbnailUrl'])
            response.insert(1, images['value'][(randint(0,len(images['value'])-1))]['thumbnailUrl'])
            response.insert(2, images['value'][(randint(0,len(images['value'])-1))]['thumbnailUrl'])
            return response

        except Exception as e:
            print e