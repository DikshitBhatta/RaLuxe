import cv2
from filters.blur import apply_blur
from functions.capture import capture_button,mouse_click
from filters.moustache import apply_moustache
from filters.glass import apply_glass

current_frame=None

def main():
   global current_frame
   
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
      faces=face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=10,minSize=(30,30))
      
      #Applying filter
      for(x,y,w,h) in faces:
         frame=apply_moustache(frame,x,y,w,h)
         
      current_frame=frame.copy() 
      button_coords=capture_button(frame)
      #Display frame
      cv2.imshow('RaLuxe',frame)
       
      cv2.setMouseCallback('RaLuxe',mouse_click,param=(*button_coords,current_frame))
      
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break   
   #Release the video capture and close windows
   cap.release()
   cv2.destroyAllWindows()      

if __name__ == "__main__":
   main()