'''
This is for observing the confidence values of yalefaces data.
Aim is to estimate accuracy.
* All the test images are assumed to be .png (not .gif)

Version of Opencv:
'''
import numpy
from PIL import Image
import posixpath

import FaceRecognizer
import cv2
import os

path = "yalefaces/"
learnedData = "testLearnerdData.yml"

print 'OpenCV vesrion: ', cv2.__version__

cascadePath = "./../haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)


# def getFaces(photo):
#     image_pil = Image.open(photo).convert('L')
#     image = numpy.array(image_pil, 'uint8')
#     faces = faceCascade.detectMultiScale(image)
#     x, y, w, h = max(faces, key=lambda (x, y, w, h): (w) * (h))
#     return image[y: y + h, x: x + w]


def getFaces(photo):
    """
    All the images are assumed not to be .gif format.
    For now took care of photo being .png format.
    """
    img = cv2.imread(photo)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # print "faces len", len(faces)
    x, y, w, h = max(faces, key=lambda (x, y, w, h): (w) * (h))
    return [gray[y: y + h, x: x + w]]
    # return faces


def TrainAllTestAll():
    os.remove(learnedData)
    faceRecognizer = FaceRecognizer.Recognizer(learnedData)
    # Training starts
    subjectId = 1
    for subject in os.listdir(path):
        # print subject
        for images in os.listdir(posixpath.join(path, subject)):
            # print images
            mappedIds = [subjectId]
            faces = getFaces(posixpath.join(posixpath.join(path, subject), images))
            faceRecognizer.update(faces, mappedIds)

        subjectId += 1

    # Testing starts
    for subject in os.listdir(path):
        # print subject
        for images in os.listdir(posixpath.join(path, subject)):
            faces = getFaces(posixpath.join(posixpath.join(path, subject), images))
            faceRecognizer.predict(faces)


def TrainManyTestOne():
    """
    Training:
    Train with many images of a subject.
    Many subjects will be in  model.
    Testing:
    Test with one image of each subject.
    :return:
    """
    os.remove(learnedData)
    faceRecognizer = FaceRecognizer.Recognizer(learnedData)

    train_images, test_images = [], []
    for subject in os.listdir(path):
        images = os.listdir(posixpath.join(path, subject))
        mappedId = int(subject[-2:])
        train_images = images[1:]
        test_images.append(posixpath.join(posixpath.join(path, subject), images[0]))

        for image in train_images:
            print "train", image, mappedId
            faces = getFaces(posixpath.join(posixpath.join(path, subject), image))
            faceRecognizer.update(faces, [mappedId])

    print "Prediction starts: "
    for image in test_images:
        print image
        faces = getFaces(image)
        faceRecognizer.predict(faces)


def TrainAllSubjectsExceptOneAndPredictThatSubject():
    os.remove(learnedData)
    faceRecognizer = FaceRecognizer.Recognizer(learnedData)

    subjects = os.listdir(path)
    train_subjects = subjects[:-1]
    test_subjec = subjects[-1]

    print train_subjects
    print test_subjec

    for subject in train_subjects:
        # print subject
        mappedId = int(subject[-2:])
        for image in os.listdir(posixpath.join(path, subject)):
            print image
            faces = getFaces(posixpath.join(posixpath.join(path, subject), image))
            faceRecognizer.update(faces, [mappedId])

    print "Prediction of images of ",test_subjec,"starts"
    for image in os.listdir(posixpath.join(path, test_subjec)):
        print image
        faces = getFaces(posixpath.join(posixpath.join(path, test_subjec), image))
        faceRecognizer.predict(faces)


# TrainAllTestAll()

TrainManyTestOne()

# TrainAllSubjectsExceptOneAndPredictThatSubject()

print os.getcwd()

print posixpath.join(os.getcwd(), path)
