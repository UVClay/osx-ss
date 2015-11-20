# OS X Screenshot Automation
# github.com/uvclay/osx-ss
# Alpha whatever it works so who cares
# Requires: fswatch, terminal-notifier

import argparse
import configparser
import os
import random
import string
import subprocess
from ftplib import FTP
from glob import glob

config = configparser.ConfigParser()
config.read('ss.ini')
_server = config['main']['Server']

# TODO: Finish arguments
"""
Pseudo
arguments: add, del/remove, edit, config, test
add: add new FTP host
del: delete existing FTP host (ensure there's a working configuration)
edit: edit any setting in a server configuration
config: change program settings (change default host, screenshot directory, etc.)
test: test configuration
#    parser = argparse.ArgumentParser(description='OSX Screenshot Utility rev-5\nwww.github.com/UVClay/osx-ss')
#    args = parser.parse_args()
"""


def main():
    execute(["fswatch", config['main']['ScreenDir']])


def upload(line):
    print(line)
    exit()
    new = gen()+'.png'
    ftp = FTP(config[_server]['FTPHost'], config[_server]['FTPUser'], config[_server]['FTPPass'])
    img = open(file, "rb")
    ftp.storbinary('STOR '+new, img)
    url = config[_server]['WebRoot']+new
    img.close()
    subprocess.Popen(["terminal-notifier", "-title", "Screenshot Uploaded!", "-message", "Image uploaded to: " + url + "", "-open", url, "-sound", "default"])
    ftp.quit()


def gen(size=5, chars=string.ascii_letters + string.digits):
    # http://stackoverflow.com/a/2257449
    return ''.join(random.choice(chars) for _ in range(size))


def exttest(line):
    #full, ext = os.path.splitext(line[:-1])
    line = line[:-1]
    print("testing {0} for .png extension".format(line))
    if line.lower().endswith(b'.png'):
        print(line.lower().endswith(b'.png'))
        print("it worked!")
        #upload(line[:-1])
    else:
        print(line.lower().endswith(b'.png'))
        print("not .png")


def execute(command):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    for line in lines_iterator:
        exttest(line)  # yield line

if __name__ == "__main__":
    main()