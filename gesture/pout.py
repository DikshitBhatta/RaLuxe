
from deepface import DeepFace
import cv2
import numpy as np

class PoutDetector:
    def __init__(self):
        # Load the pre-trained face classifier 
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect_pout(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_color = frame[y:y+h, x:x+w]
            results = DeepFace.analyze(roi_color, actions=['emotion'], enforce_detection=False)
            
            if isinstance(results, list):
                results = results[0]
            
           #detected emotions
            print(results['emotion'])

            #pout for sad and disguest emotions
            if 'emotion' in results and (results['dominant_emotion'] == 'sad' or results['dominant_emotion'] == 'disgust'):
                
                kiss_emoji = cv2.imread('filters/filter_images/kiss.png', -1)
                if kiss_emoji is not None:
                    kiss_emoji = cv2.resize(kiss_emoji, (w, h))
                    self.add_emoji(frame, kiss_emoji, (x, y))

        return frame

    def add_emoji(self, frame, emoji, position):
        x, y = position
        ex, ey, ew, eh = x, y, emoji.shape[1], emoji.shape[0]
        alpha_s = emoji[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            frame[ey:ey+eh, ex:ex+ew, c] = (alpha_s * emoji[:, :, c] + alpha_l * frame[ey:ey+eh, ex:ex+ew, c])

