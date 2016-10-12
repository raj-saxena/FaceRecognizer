# Update with your computer's IP address.
HOST_IP = "10.136.23.81"
HOST_PORT = 8080

DATABASE_FILE = "FaceRecognizer.db"
LEARNED_DATA_FILE = "LearnedData.yml"
FRONTAL_FACE_XML_FILE = "haarcascade_frontalface_default.xml"

SERIAL_PORT = "/dev/cu.usbmodem1421"
BAUD_RATE = 9600

from MapDataBase import MapDataBase

DataBase = MapDataBase(DATABASE_FILE)

from FaceRecognizer import Recognizer

faceRecognizer = Recognizer(LEARNED_DATA_FILE)
