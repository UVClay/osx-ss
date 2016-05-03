from handlers.handler import handler
import requests
from base64 import b64encode
from os import path

from imgurpython import ImgurClient

class imgur(handler):
    def __init__(self, file, server):
        handler.__init__(self, file, server)
        self.url = None
        self.apiKey = None
        self.clientId = None
        self.url = None
        self.client = None

    def setConfig(self, val):
        self.config = val
        self.clientId = self.config[self.server]['ClientId']
        self.apiKey = self.config[self.server]['ApiKey']
        self.url = self.config[self.server]['Url']
        self.client = ImgurClient(self.clientId, self.apiKey)

    def upload(self):
        resp = self.client.upload_from_path(self.file)
        print('Uploaded to imgur. %s' % resp['link'])
        return 'Uploaded %s to : %s' % (path.split(self.file)[1], resp['link'])
