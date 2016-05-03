import string
import random

class handler(object):
    def __init__(self, filename, server=None):
        self.file = filename
        self.server = server
        self.handler = self.defHandlerName()
        self.config  = None
    
    def __str__(self):
        return '%s: %s' % (self.handler, self.file )
    
    def defHandlerName(self):
        return 'Default'

    @staticmethod
    def gen(size=5, chars=string.ascii_letters + string.digits):
        # http://stackoverflow.com/a/2257449
        return ''.join(random.choice(chars) for _ in range(size))
    
    def setConfig(self, val):
        self.config = val
    
    def upload(self):
        return self.file