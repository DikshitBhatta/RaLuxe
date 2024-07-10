import cv2

def apply_moustache(frame, x, y, w, h):
    moustache_img = cv2.imread("filters/filter_images/moustache1.png", cv2.IMREAD_UNCHANGED)
    
    if moustache_img is None:
        print("Error: Could not read the moustache image")
        return frame
    
    if moustache_img.shape[2] == 4: 
        alpha = moustache_img[:, :, 3] / 255.0
        moustache_img = moustache_img[:, :, :3] 
        
        scale_factor = w / moustache_img.shape[1]
        moustache_resized = cv2.resize(moustache_img, None, fx=scale_factor/2, fy=scale_factor/2)
        
        moustache_x = x + w // 2 - moustache_resized.shape[1] // 2
        moustache_y = y + h // 2 
        
        # Overlay moustache on frame
        for c in range(3):
            frame_roi = frame[moustache_y:moustache_y + moustache_resized.shape[0], 
                              moustache_x:moustache_x + moustache_resized.shape[1], c]
            
            alpha_resized = cv2.resize(alpha, (frame_roi.shape[1], frame_roi.shape[0]))
            
            if alpha_resized.shape == moustache_resized[:, :, c].shape:
                frame_roi[:] = alpha_resized * moustache_resized[:, :, c] + (1 - alpha_resized) * frame_roi
            else:
                print(f"Error: Shapes mismatch for channel {c}. Alpha shape: {alpha_resized.shape}, Moustache shape: {moustache_resized[:, :, c].shape}")
        
        return frame
    else:
        print("Error: Moustache image does not have an alpha channel")
        return frame
