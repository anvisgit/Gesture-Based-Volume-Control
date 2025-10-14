import sys
print(sys.executable)
import cv2

import mediapipe as mp 
import pyautogui

cam = cv2.VideoCapture(0)
inphands = mp.solutions.hands.Hands()
draw = mp.solutions.drawing_utils
x0=0
x1=0
y0=0
y1=0

while True:
    i, image = cam.read()
    fheight, fwidth, _ = image.shape
    frame = cv2.flip(image, 1)
    rgbimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    output = inphands.process(rgbimage)
    hands = output.multi_hand_landmarks
    if hands:
        for h in hands:
            draw.draw_landmarks(frame, h,  mp.solutions.hands.HAND_CONNECTIONS, draw.DrawingSpec(color=(0, 0, 0), thickness=3),draw.DrawingSpec(color=(0, 0, 0), thickness=3) )
            lm = h.landmark
            for id, lm in enumerate(lm):
                x = int(lm.x * fwidth)
                y = int(lm.y * fheight)

                if id == 8: #forefinger
                    cv2.circle(img=frame, center=(x,y), radius=4, color=(0,255,0), thickness=3)
                    x0=x
                    y0=y
                if id == 4: #thumb
                    cv2.circle(img=frame, center=(x,y), radius=4, color=(0,255,0), thickness=3)
                    x1=x
                    y1=y
                cv2.line(frame,(x1,y1), (x0,y0),(0,255,0), 3 )
                d=((x0-x1)**2+(y0-y1)**2)**0.5
    
    cv2.imshow("Gesture-Based Volume Control", frame)

    key = cv2.waitKey(1)
    if key == 27:  # esc key
        break

cam.release()
cv2.destroyAllWindows()
