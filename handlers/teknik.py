from handlers.handler import handler
import requests
from base64 import b64encode

class teknik(handler):
    def upload(self):
        image = open(self.file, 'r').read()
        req = requests.post("https://api.teknik.io/v1/Upload",
            data = {
                'file':image
            })
        print(req.text)
        return