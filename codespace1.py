import sys
print(sys.executable)
import cv2
import mediapipe as mp 
import pyautogui

cam = cv2.VideoCapture(0)
inphands = mp.solutions.hands.Hands()
draw = mp.solutions.drawing_utils
x0 = x1 = y0 = y1 = 0
d = 0  # initdistance

while True:
    i, image = cam.read()
    if not i:
        break

    fheight, fwidth, _ = image.shape
    frame = cv2.flip(image, 1)
    rgbimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    output = inphands.process(rgbimage)
    hands = output.multi_hand_landmarks

    if hands:
        for h in hands:
            draw.draw_landmarks(
                frame, h, mp.solutions.hands.HAND_CONNECTIONS,
                draw.DrawingSpec(color=(0, 0, 0), thickness=3),
                draw.DrawingSpec(color=(0, 0, 0), thickness=3)
            )
            lm = h.landmark
            for id, l in enumerate(lm):
                x = int(l.x * fwidth)
                y = int(l.y * fheight)

                if id == 8:  # forefinger
                    cv2.circle(frame, (x, y), 4, (0, 255, 0), 3)
                    x0, y0 = x, y
                if id == 4:  # thumb
                    cv2.circle(frame, (x, y), 4, (0, 255, 0), 3)
                    x1, y1 = x, y

            cv2.line(frame, (x1, y1), (x0, y0), (0, 255, 0), 3)
            d = ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5

    cv2.imshow("Gesture-Based Volume Control", frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break

    
    if d > 40:
        pyautogui.press("volumeup")
    elif d > 0:
        pyautogui.press("volumedown")

cam.release()
cv2.destroyAllWindows()
