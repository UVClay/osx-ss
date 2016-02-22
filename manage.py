#!/usr/local/bin/python3
# OS X Screenshot Automation
# github.com/uvclay/osx-ss
# Revision 0.2.0
# Requires (homebrew): terminal-notifier
# Requires (linux): xclip
# Requires (pip3): pyperclip, watchdog

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
from ftplib import FTP


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
            exttest(event.src_path)
            self.observer.stop


def depcheck():
    if platform.system() == 'Darwin':
        if which('terminal-notifier') is None:
            print("Please install terminal-notifier")
            exit()
    elif platform.system() == 'Linux':
        if which('xclip') is None:
            print("Please install xclip")
            exit()
    elif platform.system() == 'Windows':
        return 0
    return 0


def main():
    path = config['main']['ScreenDir']
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


def upload(filename):
    new = gen() + '.png'
    ftp = FTP(config[_server]['FTPHost'], config[_server]['FTPUser'], config[_server]['FTPPass'])
    img = open(filename, "rb")
    ftp.storbinary('STOR ' + new, img)
    url = config[_server]['WebRoot'] + new
    img.close()
    notify(url)
    print(url)
    ftp.quit()


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


def exttest(filename):
    if filename.lower().endswith('.png'):
        upload(filename)


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
