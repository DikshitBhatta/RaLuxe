import cv2
import numpy as np

def apply_blur(image, x,y,w,h):

   cen_x,cen_y=x+w//2,y+h//2
   radius=min(w,h)//2
   
   mask=np.zeros_like(image)
   cv2.circle(mask,(cen_x,cen_y),radius,(255,255,255),-1)
   
 
   blurred_face=cv2.GaussianBlur(image,(51,51),30)
   
   combinedimage=np.where(mask == 255,blurred_face,image)
   
   return combinedimage