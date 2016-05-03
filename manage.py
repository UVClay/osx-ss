#!/usr/bin/env python3
# OS X Screenshot Automation
# github.com/uvclay/osx-ss
# Requires (homebrew): terminal-notifier
# Requires (arch): xclip, python-pyqt5
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

from handlers import ftp, imgur, pupload, handler as default

config = configparser.ConfigParser()
config.read('ss.ini')
_server = config['main']['Server']
_version = "0.5"

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
            self.observer.stop()


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

    print("OSX-SS Version: " + _version)
    print("Using uploader: " + config['main']['Handler'])
    print("Using server: " + _server)

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
    print('Found file [%s]' % filename)
    user_handler = config['main']['Handler']
    data = [filename, _server]
    if user_handler == 'pupload':
        handler = pupload.pupload(*data)
    elif user_handler == 'ftp':
        handler = ftp.ftp(*data)
    elif user_handler == 'imgur':
        handler = imgur.imgur(*data)
    elif user_handler == 'debug':
        handler = default.handler(*data)
    else:
        return
    handler.setConfig(config)
    notify(handler.upload())
    return



def notify(url):
    if not url:
        return

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
    return


def which(program):
    def is_exe(fpath):
        #return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        return True

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
