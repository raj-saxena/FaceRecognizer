import cv2
def getBigRectangle( faces):
        print max(faces, key=lambda (x, y, w, h): (w) * (h))
        return max(faces, key=lambda (x, y, w, h): (w) * (h))


FRONTAL_FACE_XML_FILE = "haarcascade_frontalface_default.xml"
img = cv2.imread("ImageToCrop.png")
gray =img
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faceCascade = cv2.CascadeClassifier(FRONTAL_FACE_XML_FILE)
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(100, 100),
    flags=cv2.CASCADE_SCALE_IMAGE
)

if len(faces):
    (x, y, w, h) = getBigRectangle(faces)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    face = gray[y:y + h, x:x + w]
    cv2.imwrite("CroppedImage.png",face)
