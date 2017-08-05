import sys

from PyQt4 import QtGui

from Constants import faceRecognizer
from FaceRecognizerWindow import FaceRecognizerWindow

print sys.argv
import sqlite3

from Constants import DataBase

app = QtGui.QApplication(sys.argv)
Photos = []
w = FaceRecognizerWindow(Photos, 2, 2, None)
w.setWindowTitle('Face Recognizer')
w.show()
app.exec_()

# print Photos

print sys.argv[1]
if len(sys.argv) < 2:
    print "Invalid Action"  # Empty string is False
else:
    uuid = sys.argv[1]
    try:
        mappedId = DataBase.add(uuid)
        labels = [mappedId for i in range(len(Photos))]
        faceRecognizer.update(Photos, labels)
        print "Trained for " + uuid + " =>" + str(mappedId)
    except sqlite3.IntegrityError:
        print "User with uuid=%s already exists,"  # initiating re-training."
