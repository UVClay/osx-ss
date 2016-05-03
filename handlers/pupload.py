import subprocess
from os import path
import handler

class pupload(handler):
    def upload(self):
        # TODO: Make this less horrible.  Its really gross.
        url = self.config[self.server]['PupFile']
        conckey = self.config[self.server]['PupKey1'] + "=" + self.config[self.server]['PupKey2']
        concfile = "file[]=@" + path.abspath(self.filename)
        c = subprocess.Popen(
            ["curl", "-s", "-F", conckey, "-F", concfile, url], stdout=subprocess.PIPE
        )
        for line in iter(c.stdout.readline, ''):
            stream = line.decode()
            if stream == '':
                pass
            else:
                print(stream)
                c.kill()
                return stream
        return