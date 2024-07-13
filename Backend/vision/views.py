from django.shortcuts import render
import cv2
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .filters.moustache import apply_moustache

@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        try:
            file = request.FILES['image']
            image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
            
            if image is None:
                return JsonResponse({'error': 'Invalid image'}, status=400)
            
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(30,30))
            
            for (x, y, w, h) in faces:
                image = apply_moustache(image, x, y, w, h)
            
            _, buffer = cv2.imencode('.jpg', image)
            response = buffer.tobytes()
            return JsonResponse({'image': response}, safe=False)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
