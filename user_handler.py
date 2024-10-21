import pickle
import cv2

class UserData:
	def __init__(self):
		self.name = 'None'
		self.gender = 'None'
		self.userphoto = 0

	def extractData(self):
		with open('userData/userData.pck', 'rb') as file:
			details = pickle.load(file)
			self.name, self.gender, self.userphoto = details['name'], details['gender'], details['userphoto']

	def updateData(self, name, gender, userphoto):
		with open('userData/userData.pck', 'wb') as file:
			details = {'name': name, 'gender': gender, 'userphoto': userphoto}
			pickle.dump(details, file)

	def getName(self):
		return self.name

	def getGender(self):
		return self.gender

	def getUserPhoto(self):
		return self.userphoto

def UpdateUserPhoto(avatar):
	u = UserData()
	u.extractData()
	u.updateData(u.getName(), u.getGender(), avatar)
# user_handler.py

import cv2

def face_unlocker():
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Load the face classifier
    face_classifier = cv2.CascadeClassifier('Cascade/haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            # If a face is detected, you could return True
            cap.release()
            cv2.destroyAllWindows()
            return True
		
        
        cv2.imshow('Face Unlocker', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False
