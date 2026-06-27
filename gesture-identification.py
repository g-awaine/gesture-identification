import modules as m
import mediapipe as mp
import cv2 as cv

# Initialise the webcam
webcam = m.Webcam(cam=0)

#detects hand object and draws
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

calling = [0, None]
frames_to_call = 5
while True:
    # Get the frame
    frame = webcam.get_frame()

    results = hands.process(frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb = m.finger_up(hand_landmarks, 4, 3)
            index = m.finger_up(hand_landmarks, 8, 6)
            middle = m.finger_up(hand_landmarks, 12, 10)
            ring = m.finger_up(hand_landmarks, 16, 14)
            pinky = m.finger_up(hand_landmarks, 20, 18)
            thumb = m.finger_up(hand_landmarks, 4, 1)

            gesture = None

            if index and not middle and not ring and not pinky:
                gesture = "index_up"

            if not index and middle and ring and pinky:
                gesture = 'index_down'

            if middle and not index and not ring and not pinky:
                webcam.release()
                break

            if calling[1] == gesture:
                calling[0] += 1
            else:
                calling = [1, gesture]

            if calling[0] == frames_to_call:
                if gesture in m.gesture_actions:
                    m.gesture_actions[gesture]()
                    calling = [0, None]

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # Shows frame
    webcam.show_frame(frame)

    # Releases cameras and destroys windows
    if cv.waitKey(1) == ord('q'):
        webcam.release()
        break
