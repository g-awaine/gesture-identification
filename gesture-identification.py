from modules import Webcam
import cv2 as cv

# Initialise the webcam
webcam = Webcam(cam=0)

while True:
    # Get the frame
    frame = webcam.get_frame()

    # Shows frame
    webcam.show_frame(frame)

    # Releases cameras and destroys windows
    if cv.waitKey(1) == ord('q'):
        webcam.release()
        break

