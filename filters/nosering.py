import cv2

def apply_nosering(frame,x,y,w,h):
   
   ring_img=cv2.imread("filters/filter_images/nosering1.png",cv2.IMREAD_UNCHANGED)
   
   if ring_img is None:
      print("Filter not found")
      return frame

   #checking for alpha channel
   if ring_img.shape[2]==4:
      alpha=ring_img[:,:,3]/255.0
      ring_img=ring_img[:,:,:3]
      
      scalefactor=(w/ring_img.shape[0])/8
      ring_resized=cv2.resize(ring_img,None,fx=scalefactor,fy=scalefactor)
     
   
      ring_x = x+w//2 - ring_resized.shape[1]//2
      ring_y = int(y + h//1.5)
      
      for c in range(3):
         frame_roi=frame[ring_y:ring_y+ring_resized.shape[0],ring_x:ring_x+ring_resized.shape[1],c]
         
         alpha_resized=cv2.resize(alpha,(frame_roi.shape[1],frame_roi.shape[0]))
         
         if alpha_resized.shape==ring_resized[:,:,c].shape:
            frame_roi[:]=alpha_resized*ring_resized[:,:,c]+(1-alpha_resized)*frame_roi
         else:
            print("Shape doesn't match")
      return frame
   else:
      print("Moustache image doesn't have an alpha channel")
      return frame
         
            
      
      
      
   