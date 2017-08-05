import sys
from collections import Counter

from PyQt4 import QtGui

from Constants import faceRecognizer
from FaceRecognizerWindow import FaceRecognizerWindow

print sys.argv

from Constants import DataBase

# if len(sys.argv) < 2:
#     print "Invalid Action"  # Empty string is False
#     sys.exit()

app = QtGui.QApplication(sys.argv)
Photos = []
w = FaceRecognizerWindow(Photos, 2, 2, None)
w.setWindowTitle('Face Recognizer')
w.show()
app.exec_()

# print Photos
if len(Photos) != 0:
    predicted = faceRecognizer.predict(Photos)
    data = Counter(predicted)
    predictedFace = data.most_common(1)[0][0]
    # print "Predicted", data.most_common(1)[0][0]
    result = DataBase.getUuid(predictedFace)
    # print 'result', result
    if result is not None:
        print "You are %s" % (result[0],)
    else:
        print "UnRegistered"
