import unittest
import FaceRecognizer
import pickle


class FaceRecognizerTest(unittest.TestCase):
    def test_shouldReturn(self):
        faceRecognizer = FaceRecognizer.Recognizer("testLearnerdData.yml")

        for i in range(1,3):
            file = open("../Imgs/"+str(i)+".txt","r")
            photos = pickle.load(file)
            print photos
            labels = [i for w in range(len(photos))]
            faceRecognizer.update(photos,labels)
            file.close()

        for i in range(1,3):
            file = open("../Imgs/Single/"+str(i)+".txt","r")
            photos = pickle.load(file)
            print photos
            expected = [i for w in range(len(photos))]
            predicted = faceRecognizer.predict(photos)
            file.close()
            self.assertEqual(expected,predicted)

if __name__ == "__main__":
    unittest.main()
