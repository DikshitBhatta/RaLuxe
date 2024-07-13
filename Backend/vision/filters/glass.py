import cv2

def apply_glass(frame,x,y,w,h):
   glass_img=cv2.imread("filters/filter_images/glass2.png",cv2.IMREAD_UNCHANGED)
   
   if glass_img is None:
      print("Filter not found")
      return frame
   
   if glass_img.shape[2]==4:
      alpha=glass_img[:,:,3]/255.0
      glass_img=glass_img[:,:,:3]
      
   
      scalefactor=((w/glass_img.shape[1])/1.1)
      glass_resized=cv2.resize(glass_img, None,fx=scalefactor,fy=scalefactor)
      alpha_resized=cv2.resize(alpha,(glass_resized.shape[1],glass_resized.shape[0]))
   
      glass_x=x+w//2-glass_resized.shape[1]//2
      glass_y=int(y+h//3.95)
   
   #overlay
      for c in range(3):
         frame_roi = frame[glass_y:glass_y + glass_resized.shape[0], glass_x:glass_x + glass_resized.shape[1], c]
         
      
         if frame_roi.shape[:2] == alpha_resized.shape:
            frame_roi[:]= alpha_resized*glass_resized[:,:,c]+(1-alpha_resized)*frame_roi
         else:
            print("Shape mismatch") 
      return frame
   else:
        print("Error: Moustache image does not have an alpha channel")
        return frame