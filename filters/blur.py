import cv2

def apply_blur(frame, x,y,w,h):
   face_region=frame[y:y+h,x:x+w]
   blurred_face=cv2.GaussianBlur(face_region,(99,99),39)
   frame[y:y+h,x:x+w]=blurred_face
   return frame