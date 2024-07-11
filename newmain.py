# main.py
from gesture.pout import PoutDetector
import cv2

def main():
    detector = PoutDetector()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = detector.detect_pout(frame)
        cv2.imshow('Pout Detector', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
