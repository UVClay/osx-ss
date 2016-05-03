from handlers.handler import handler
import requests
from base64 import b64encode
from os import path

class imgur(handler):
    def __init__(self, file, server):
        handler.__init__(self, file, server)
        self.url = None
        self.apiKey = None
        self.clientId = None
        self.url = None

    def setConfig(self, val):
        self.config = val
        self.clientId = self.config[self.server]['ClientId']
        self.apiKey = self.config[self.server]['ApiKey']
        self.url = self.config[self.server]['Url']

    def upload(self):
        image = b64encode(open(self.file, 'rb').read())
        name = path.split(self.file)[1]

        imgur_req = requests.post(
            self.url,
            headers = {'Authorization' : 'Client-ID %s' % self.clientId},
            data = {
                'image': image
            }
        )
        print(imgur_req.text)
        return 'done'
