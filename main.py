import cv2
from filters.blur import apply_blur

def main():
   cap=cv2.VideoCapture(0) #video capture
   if not cap.isOpened():
      print("Error: Camera is not opened")
      return
   
   face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml') #haarcascade model call
   
   while True:
      ret, frame=cap.read() # reading the fram from the video
      if not ret:
         print("Failed to capture image")
         break
      
      gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  #CONVERT FRAME TO GRAYSCALE
      faces=face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30))
      
      #Applying filter
      for(x,y,w,h) in faces:
         frame=apply_blur(frame,x,y,w,h)
         
      #Display frame
      cv2.imshow('Webcam',frame)
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break   
   #Release the video capture and close windows
   cap.release()
   cv2.destroyAllWindows()      

if __name__ == "__main__":
   main()