import sys
from PyQt4 import QtGui

def main():
    app = QtGui.QApplication(sys.argv)

    trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon("../icon.png"), app)
    menu = QtGui.QMenu()
    exitAction = menu.addAction("Exit")
    trayIcon.setContextMenu(menu)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()