import cv2 as cv
import numpy as np
import mediapipe as mp
import pyautogui
x1=0
y1=0
x2=0
y2=0

webcam = cv.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils


while True:
    _, image = webcam.read()
    image = cv.flip(image,1)
    frame_height ,frame_width,_ = image.shape
    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(
                image,
                hand,
                mp.solutions.hands.HAND_CONNECTIONS,
                drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2),
                drawing_utils.DrawingSpec(color=(255, 0, 0), thickness=4)
            )

            landmarks = hand.landmark

            for id,landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv.circle(img = image,center=(x,y),radius=8,color=(255,0,0),thickness=3)
                    x1=x
                    y1=y
                if id == 4:
                        cv.circle(img=image, center=(x, y),radius=8,color=(255,0,0),thickness=3)
                        x2=x
                        y2=y
        dist = ((x2-x1)**2 + (y2-y1)**2)**(0.5)//4
        cv.line(image,(x1,y1),(x2,y2),(0,255,0),2)
        if dist>30:
            pyautogui.press('volumeup')
        else:
            pyautogui.press('volumedown')
    cv.imshow('Volume Controller using HAND', image)
    key = cv.waitKey(10)
    if key == 27:
        break
webcam.release()
cv.destroyAllWindows()