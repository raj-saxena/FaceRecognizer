from collections import Counter
from PyQt4 import QtGui
from multiprocessing import Process, Manager

from FaceRecognizerWindow import FaceRecognizerWindow
from Constants import faceRecognizer


def recognizeFace():
    predictedFace = 0
    photos = getPhotos("Test", 4, 2)
    print photos
    if len(photos) != 0:
        predicted = faceRecognizer.predict(photos)
        data = Counter(predicted)
        print "Predicted", data.most_common(1)[0][0]
        predictedFace = data.most_common(1)[0][0]
    return predictedFace


def trainForFace(label):
    photos = getPhotos("Train", 8, 2)
    labels = [label for i in range(len(photos))]
    faceRecognizer.update(photos, labels)
    print "captured and trained for => " + str(labels)


def getPhotos(Title, numberOfFrames, delay):
    manager = Manager()
    sharedList = manager.list()
    p = Process(target=readFrames, args=(Title, numberOfFrames, delay, sharedList,))
    p.start()
    p.join()
    return list(sharedList)


def readFrames(Title, numberOfFrames, delay, sharedList):
    photos = []
    app = QtGui.QApplication([Title])
    w = FaceRecognizerWindow(photos, numberOfFrames, delay, None)
    w.setWindowTitle(Title)
    w.show()
    app.exec_()
    for w in photos:
        sharedList.append(w)


if __name__ == '__main__':
    pass
    # trainForFace(1)
