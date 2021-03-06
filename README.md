## OS X Screenshot Utility (osx-ss)
OS X Screenshot Utility is a simple Python daemon leveraging watchdog to monitor your screenshots folder and upload any new screenshots to an FTP host, Imgur, or [puploader][puploader] host.  Designed to help fill the gap left by ShareX on my Mac machines.

## Installation and usage:
*current version:* 0.3.0

    git clone https://github.com/UVClay/osx-ss
    chmod +x manage.py
    <Update ss.ini properly, automated solution soon>
    python3 manage.py
    Leave your terminal window open (or python3 manage.py &)

## To Do:
* Mime fingerprinting
* Come up with a new name
* launchctl daemon script
* Installer
* Finish arguments/interactive logic
* Logic for additional file types
* Built-in support for image hosts (pomf, etc.)
* Built-in support for cloud file hosting (box, mega, aws, etc.)
* Support for non-FTP file transfer (sftp, POST, rsync)

## Wishlist:
* /!\ GUI /!\
* Notification area icons
* Windows support

## Thanks to:
* [watchdog][watchdog]
* [terminal-notifier][terminal-notifier]
* [sides][sides]

[terminal-notifier]: https://github.com/julienXX/terminal-notifier
[watchdog]: https://github.com/gorakhargosh/watchdog
[sides]: https://github.com/sides
[puploader]: https://github.com/sides/puploader
