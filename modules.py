import cv2 as cv

class Webcam():
    def __init__(self, cam:int=0):
        self.cap = cv.VideoCapture(cam)
        if not self.cap.isOpened():
            print("Cannot open camera")
            raise ValueError("Cannot get camera")

    def get_frame(self):
        # Capture frame-by-frame
        ret, frame = self.cap.read()
        
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?)")
            raise ValueError("No frame")
        
        return frame
        
    def show_frame(self, frame):
        # Display the frame
        cv.imshow('Gesture Detection', frame)

    
    def release(self): 
        # When everything done, release the capture
        self.cap.release()
        cv.destroyAllWindows()
