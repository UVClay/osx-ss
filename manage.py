#!/usr/local/bin/python3
# OS X Screenshot Automation
# github.com/uvclay/osx-ss
# Revision 0.2.0
# Requires (homebrew): terminal-notifier
# Requires (linux): xclip
# Requires (pip3): pyperclip, watchdog
# Optional (pip3): pycurl

import configparser
import os
import platform
import pyperclip
import random
import string
import subprocess
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

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


class Monitor(FileSystemEventHandler):
    def __init__(self, observer, filename):
        self.observer = observer
        self.filename = filename

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(self.filename):
            handler(event.src_path)
            self.observer.stop


def depcheck():
    if platform.system() == 'Darwin':
        if which('terminal-notifier') is None:
            print("Please install terminal-notifier")
            exit()
        if which('curl') is None:
            print("curl isn't installed.  However you managed that.  Install it.")
            exit()
    elif platform.system() == 'Linux':
        if which('xclip') is None:
            print("Please install xclip")
            exit()
        if which('curl') is None:
            print("Please install curl")
            exit()
    elif platform.system() == 'Windows':
        return 0
    return 0


def main():
    path = config['main']['WDir']
    filename = ''

    observer = Observer()
    event_handler = Monitor(observer, filename)

    observer.schedule(event_handler, path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    return 0


def handler(filename):
    if config['main']['Handler'] == 'pupload':
        pupload_upload(filename)
    elif config['main']['Handler'] == 'ftp':
        ftp_upload(filename)
    elif config['main']['Handler'] == 'debug':
        debug(filename)
    else:
        return


def ftp_upload(filename):
    from ftplib import FTP
    ext = os.path.splitext(os.path.abspath(filename))[-1]
    new = gen() + ext
    ftp = FTP(config[_server]['FTPHost'], config[_server]['FTPUser'], config[_server]['FTPPass'])
    img = open(filename, "rb")
    ftp.storbinary('STOR ' + new, img)
    url = config[_server]['WebRoot'] + new
    img.close()
    notify(url)
    print(url)
    ftp.quit()


'''
def pupload_upload(filename):
    import pycurl
    from urllib.parse import urlencode
    file = config[_server]['PupFile']
    key1 = config[_server]['PupKey1']
    key2 = config[_server]['PupKey2']

    c = pycurl.Curl()
    c.setopt(c.URL, file)

    c.setopt(c.POSTFIELDS, urlencode({key1: key2}))
    c.setopt(c.HTTPPOST, [
    ('file[]', (
        c.FORM_FILE, __file__,
    )),
])

    c.perform()
    c.close()
'''


def pupload_upload(filename):
    # TODO: Make this less horrible.  Its really gross.
    url = config[_server]['PupFile']
    conckey = config[_server]['PupKey1'] + "=" + config[_server]['PupKey2']
    concfile = "file[]=@" + os.path.abspath(filename)
    c = subprocess.Popen(
        ["curl", "-s", "-F", conckey, "-F", concfile, url], stdout=subprocess.PIPE
    )
    for line in iter(c.stdout.readline, ''):
        stream = line.decode()
        if stream == '':
            pass
        else:
            notify(stream)
            c.kill()
            return


def gen(size=5, chars=string.ascii_letters + string.digits):
    # http://stackoverflow.com/a/2257449
    return ''.join(random.choice(chars) for _ in range(size))


def notify(url):
    if platform.system() == 'Darwin':
        subprocess.Popen(
            ["terminal-notifier", "-title", "Screenshot Uploaded!", "-message", "Image uploaded to: " + url + "",
             "-open", url, "-sound", "default"])
    elif platform.system() == 'Linux':
        subprocess.Popen(
            ["notify-send", "-i", "icon-jpeg", "Screenshot Uploaded!", "Image uploaded to: " + url + ""])
    elif platform.system() == 'Windows':
        print("whee")
    pyperclip.copy(url)


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


if __name__ == "__main__":
    depcheck()
    main()
