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
game = False
frames = 0
prev_x = None
prev_y = None


while True:
    # Get the frame
    frame = webcam.get_frame()

    results = hands.process(frame)
    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks,results.multi_handedness):
            thumb = m.finger_up(hand_landmarks, 4, 3)
            index = m.finger_up(hand_landmarks, 8, 6)
            middle = m.finger_up(hand_landmarks, 12, 10)
            ring = m.finger_up(hand_landmarks, 16, 14)
            pinky = m.finger_up(hand_landmarks, 20, 18)
            thumb = m.finger_up(hand_landmarks, 4, 1)

            gesture = None
            hand = handedness.classification[0].label

            #Gestures for right hand just for increasing/decreasing volume
            if hand == "Left":
                if index and not middle and not ring and not pinky:
                    gesture = "index_up"

                if not index and middle and ring and pinky:
                    gesture = 'index_down'

                if pinky and not index and not ring and not middle:
                    webcam.release()
                    break

            #Gestures for left hand, for motion detection, just to see how still you can keep your hand
            if hand == "Right":
                if index and middle and ring and pinky and not game:
                    game = True
                    frames = 0
                    prev_x = None
                    prev_y = None

                if game:
                    wristx, wristy = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
                    frames += 1

                if prev_x is not None:
                    dx = wristx - prev_x
                    dy = wristy - prev_y

                    if abs(dx) > 0.05 or abs(dy) > 0.05:
                        print("Moved!")
                        print("Held still for:", frames)

                        game = False
                        frames = 0

                prev_x = wristx
                prev_y = wristy

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
