import cv2
import numpy as np
import time
import mediapipe as mp
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

exercise = ("shoulder_press")  # Change to "front_raises", "shoulder_press", "squats", "lunges", "high_knees"

while True:
    success, img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        color = (255, 0, 255)
        angle = 0
        per = 0
        bar = 0

        if exercise == "curls":
            angle = detector.findAngle(img, 12, 14, 16)  # Right arm
            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (210, 310), (650, 100))

        elif exercise == "lateral_raises":
            angle = detector.findAngle(img, 24, 12, 14)  # Angle at shoulder
            per = np.interp(angle, (70, 170), (0, 100))
            bar = np.interp(angle, (70, 170), (650, 100))

        elif exercise == "front_raises":
            angle = detector.findAngle(img, 24, 12, 16)
            per = np.interp(angle, (70, 160), (0, 100))
            bar = np.interp(angle, (70, 160), (650, 100))

        elif exercise == "shoulder_press":
            angle = detector.findAngle(img, 24, 12, 14)
            per = np.interp(angle, (60, 170), (0, 100))
            bar = np.interp(angle, (60, 170), (650, 100))

        elif exercise == "squats":
            angle = detector.findAngle(img, 24, 26, 28)
            per = np.interp(angle, (90, 170), (100, 0))
            bar = np.interp(angle, (90, 170), (100, 650))

        elif exercise == "lunges":
            angle = detector.findAngle(img, 24, 26, 28)
            per = np.interp(angle, (90, 170), (100, 0))
            bar = np.interp(angle, (90, 170), (100, 650))

        elif exercise == "high_knees":
            if lmList[26][2] < lmList[24][2]:
                per = 100
            else:
                per = 0
            bar = np.interp(per, (0, 100), (650, 100))

        # Rep Counting Logic
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        # Progress Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f"PERCENTAGE: {int(per)}%", (800, 75), cv2.FONT_HERSHEY_PLAIN, 3, color, 2)

        # Count Display
        cv2.putText(img, f"COUNT: {int(count)}", (45, 670), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Show
    cv2.imshow("Live Video", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
