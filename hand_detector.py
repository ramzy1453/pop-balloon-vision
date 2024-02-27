import mediapipe as mp
import cv2 as cv
import numpy as np

class HandDetector:
    def __init__(self, max_hands=2, min_detection_confidence=0.8) -> None:

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_hands,
                                         min_detection_confidence=min_detection_confidence)

        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, flip_type=True, draw=True):
        frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(frameRGB)
        all_hands = []
        h, w, c = frame.shape

        if self.results.multi_hand_landmarks:
            for handType, landmarks in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                hand = {}
                landmarks_list = []
                x_list = []
                y_list = []
                for lm in landmarks.landmark:
                    px, py = int(lm.x * w), int(lm.y * h)
                    landmarks_list.append([px, py])
                    x_list.append(px)
                    y_list.append(py)

                # Bounding Box
                xmin, xmax = min(x_list), max(x_list)
                ymin, ymax = min(y_list), max(y_list)
                boxW, boxH = xmax - xmin, ymax - ymin
                
                bbox = xmin, ymin, boxW, boxH
                
                cx, cy = bbox[0] + (bbox[2] // 2), bbox[1] + (bbox[3] // 2)

                hand["landmarks_list"] = landmarks_list
                hand["bbox"] = bbox
                hand["center"] = (cx, cy)

                if flip_type:
                    if handType.classification[0].label == "Right":
                        hand["type"] = "Left"
                    else:
                        hand["type"] = "Right"
                else:
                    hand["type"] = handType.classification[0].label
                all_hands.append(hand)

                # Draw
                if draw:
                    self.mp_draw.draw_landmarks(frame, landmarks,
                                               self.mp_hands.HAND_CONNECTIONS)
                    cv.rectangle(frame, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (255, 0, 255), 2)
                    cv.putText(frame, hand["type"], (bbox[0] - 30, bbox[1] - 30), cv.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
        return all_hands, frame
        