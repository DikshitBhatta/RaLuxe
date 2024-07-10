import cv2
import numpy as np
import os
from datetime import datetime


def capturephoto(frame):
   
   os.makedirs("capture_photoes",exist_ok=True)
   
   timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
   
   filename=os.path.join("capture_photoes",f"filteredphoto_{timestamp}.jpg")
   
   if isinstance(frame,np.ndarray):
      cv2.imwrite(filename,frame)
      print(f"saved {filename} !")
   else:
      print("Error: Frame is not a valid image")
   
def capture_button(frame):
   #button properties
   frame_height,frame_width,_=frame.shape
   btn_text="Capture"
   
   cen_x=frame_width//2
   cen_y=frame_height-40
   radius=60
   #button
   cv2.circle(frame,(cen_x,cen_y),radius,(0,255,0),-1)
   cv2.putText(frame,btn_text,(cen_x-25,cen_y+5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
   
   return(cen_x,cen_y,radius)

def mouse_click(event,x,y,flags,param):
   if event==cv2.EVENT_LBUTTONDOWN:
      cen_x,cen_y,radius,current_frame=param
      if(x-cen_x) ** 2 + (y-cen_y)**2 <= radius**2:
         capturephoto(current_frame)
   