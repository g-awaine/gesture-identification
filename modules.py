import cv2 as cv
from pycaw.pycaw import AudioUtilities

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

#Volume control
device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume

def volume_up(step=0.05):
    current = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(min(current + step, 1.0), None)

def volume_down(step=0.05):
    current = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(max(current - step, 0.0), None)
#-----------------------------------------------------

#Functions for each hand sign
def finger_up(hand, tip, pip):
    return hand.landmark[tip].y < hand.landmark[pip].y
#-----------------------------------------------------

#Dictionary representing what to do
gesture_actions = {
    "index_down": volume_down,
    "index_up": volume_up,
}
#------------------------------------------------------