from handlers.handler import handler

from ftplib import FTP
from os import path

class ftp(handler):
    def defHandlerName(self):
        return 'ftp'
    
    def upload(self):
        config = self.config
        print(config)
        ext = path.splitext(path.abspath(self.file))[-1]
        new = self.gen() + ext
        Ftp = FTP(config[self.server]['FTPHost'], config[self.server]['FTPUser'], config[self.server]['FTPPass'])
        img = open(self.file, "rb")
        Ftp.storbinary('STOR ' + new, img)
        url = config[self.server]['WebRoot'] + new
        img.close()
        print(url)
        Ftp.quit()
        return url