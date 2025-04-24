import cv2
import numpy as np
import time
import mediapipe as mp
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count1 = 0  # For elbow curl
count2 = 0  # For shoulder motion
dir1 = 0
dir2 = 0
pTime = 0

while True:
    success, img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        # ----------- TRACKER 1: ELBOW CURL -----------
        angle1 = detector.findAngle(img, 12, 14, 16)  # Shoulder - Elbow - Wrist
        per1 = np.interp(angle1, (180, 300), (0, 100))
        bar1 = np.interp(angle1, (180, 300), (650, 100))

        color1 = (255, 0, 255)
        if per1 == 100:
            color1 = (0, 255, 0)
            if dir1 == 0:
                count1 += 0.5
                dir1 = 1
        if per1 == 0:
            color1 = (0, 255, 0)
            if dir1 == 1:
                count1 += 0.5
                dir1 = 0

        # ----------- TRACKER 2: SHOULDER MOTION -----------
        angle2 = detector.findAngle(img, 24, 12, 14)  # Hip - Shoulder - Elbow
        per2 = np.interp(angle2, (40, 120), (0, 100))  # Adjust this range if needed
        bar2 = np.interp(angle2, (40, 120), (650, 100))

        color2 = (255, 255, 0)
        if per2 == 100:
            color2 = (0, 255, 255)
            if dir2 == 0:
                count2 += 0.5
                dir2 = 1
        if per2 == 0:
            color2 = (0, 255, 255)
            if dir2 == 1:
                count2 += 0.5
                dir2 = 0

        # ----------- DRAW BARS -----------
        # Elbow Curl Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color1, 3)
        cv2.rectangle(img, (1100, int(bar1)), (1175, 650), color1, cv2.FILLED)
        cv2.putText(img, f"Curl: {int(per1)}%", (950, 75), cv2.FONT_HERSHEY_PLAIN, 2, color1, 2)

        # Shoulder Motion Bar
        cv2.rectangle(img, (1000, 100), (1075, 650), color2, 3)
        cv2.rectangle(img, (1000, int(bar2)), (1075, 650), color2, cv2.FILLED)
        cv2.putText(img, f"Shoulder: {int(per2)}%", (750, 75), cv2.FONT_HERSHEY_PLAIN, 2, color2, 2)

        # ----------- COUNTS DISPLAY -----------
        cv2.putText(img, f"Curl Count: {int(count1)}", (50, 630), cv2.FONT_HERSHEY_PLAIN, 2, color1, 2)
        cv2.putText(img, f"Shoulder Count: {int(count2)}", (50, 670), cv2.FONT_HERSHEY_PLAIN, 2, color2, 2)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.imshow("Live Video", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
