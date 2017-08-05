from PyQt4 import QtCore, QtGui, uic
import sys
import cv2
import time

from Constants import FRONTAL_FACE_XML_FILE


form_class = uic.loadUiType("simple.ui")[0]


class OwnImageWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(OwnImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()


class FaceRecognizerWindow(QtGui.QMainWindow, form_class):
    def __init__(self, photos, noOfFrames, interval, parent=None):
        QtGui.QMainWindow.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.faceCascade = cv2.CascadeClassifier(FRONTAL_FACE_XML_FILE)

        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.capture.set(cv2.CAP_PROP_FPS, 30)

        self.window_width = self.ImgWidget.frameSize().width()
        self.window_height = self.ImgWidget.frameSize().height()
        self.ImgWidget = OwnImageWidget(self.ImgWidget)

        self.noOfFrames = noOfFrames
        self.interval = interval
        self.photos = photos

        self.time = time.time()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

    def update_frame(self):
        currentTime = time.time()
        # print len(self.photos)
        if len(self.photos) == self.noOfFrames:
            self.capture.release()
            cv2.destroyAllWindows()
            QtCore.QCoreApplication.instance().quit()

        if len(self.photos) == self.noOfFrames:
            # Because of latency in closing this function might called even quit is called.
            return

        isFrameReadCorrectly, img = self.capture.read()

        if isFrameReadCorrectly:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            if len(faces):
                (x, y, w, h) = self.getBigRectangle(faces)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # self.photos.append((x, y, w, h))
                if currentTime - self.time >= self.interval:
                    self.photos.append(gray[y:y + h, x:x + w])
                    self.time = time.time()

        img_height, img_width, img_colors = img.shape
        scale_w = float(self.window_width) / float(img_width)
        scale_h = float(self.window_height) / float(img_height)
        scale = min([scale_w, scale_h])

        if scale == 0:
            scale = 1

        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, bpc = img.shape
        bpl = bpc * width
        image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888)
        self.ImgWidget.setImage(image)

    def getBigRectangle(self, faces):
        # print max(faces, key=lambda (x, y, w, h): (w) * (h))
        return max(faces, key=lambda (x, y, w, h): (w) * (h))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    Photos = []
    w = FaceRecognizerWindow(Photos, 15, 2, None)
    w.setWindowTitle('Face Recognizer')
    w.show()
    app.exec_()

    print Photos

    cv2.namedWindow('frame')
    i=0
    for photo in Photos:
        cv2.imwrite('frame'+str(i)+".png", photo)
        i+=1
        # cv2.waitKey(60)
