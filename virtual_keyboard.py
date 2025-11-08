import cv2
import pyautogui
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    ["SPACE", "BACK"]
]

class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

def draw_transparent_keyboard(img, buttonList, alpha=0.3):
    overlay = img.copy()
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 180, 255), -1)  # cyan-blue tone
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 255, 255), 2)  # border

        cv2.putText(overlay, button.text, (x + 20, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)  # shadow
        cv2.putText(overlay, button.text, (x + 20, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)  # white text

    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    return img

finalText = ""
cooldown_frames = 0

print("Virtual Keyboard started. Use Thumb + Index to click, Thumb + Pinky to exit.")

while True:
    success, img = cap.read()
    if not success:
        continue
    img = cv2.flip(img, 1)

    img = cv2.GaussianBlur(img, (7, 7), 0)

    hands, img = detector.findHands(img)
    img = draw_transparent_keyboard(img, buttonList, alpha=0.35)

    if hands:
        lmList = hands[0]["lmList"]

        if len(lmList) >= 21:
            
            x1, y1 = lmList[4][0:2]
            x2, y2 = lmList[8][0:2]
            distance, _, _ = detector.findDistance((x1, y1), (x2, y2), img)
            cv2.circle(img, (x1, y1), 10, (255, 255, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 255, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 2)

            for button in buttonList:
                bx, by = button.pos
                bw, bh = button.size

                if bx < x2 < bx + bw and by < y2 < by + bh:
                    cv2.rectangle(img, (bx, by), (bx + bw, by + bh), (0, 255, 255), 2)
                    if distance < 45 and cooldown_frames == 0:
                        key_pressed = button.text
                        cooldown_frames = 20

                        if key_pressed == "SPACE":
                            pyautogui.press("space")
                        elif key_pressed == "BACK":
                            pyautogui.press("backspace")
                        else:
                            pyautogui.typewrite(key_pressed.lower())

                        cv2.rectangle(img, (bx, by), (bx + bw, by + bh), (0, 100, 255), -1)
                        cv2.putText(img, key_pressed, (bx + 20, by + 60),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                        print(f"Pressed: {key_pressed}")

  
            tx, ty = lmList[4][0:2]
            px, py = lmList[20][0:2]
            exit_dist, _, _ = detector.findDistance((tx, ty), (px, py), img)
            if exit_dist < 40:
                print("Exit gesture detected. Closing Virtual Keyboard...")
                break

    if cooldown_frames > 0:
        cooldown_frames -= 1
    cv2.imshow("Virtual Keyboard", img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
print(" Virtual Keyboard closed safely.")
