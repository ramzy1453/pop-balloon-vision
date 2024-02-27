from time import time
import cv2 as cv

old_time = time()

def draw_fps(frame):
    global old_time
    current_time = time()
    fps = 1 / (current_time - old_time)
    old_time = current_time
    cv.putText(
        frame, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3
    )
    return old_time
