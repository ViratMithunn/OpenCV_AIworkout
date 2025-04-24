import cv2
import numpy as np
import time
import mediapipe as mp
import PoseModule as pm

cap = cv2.VideoCapture(0) # Outside camera is 1; inbuilt is 0
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

while True:
    success, img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #img = cv2.resize(img, (1280,720))
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    #print(lmList)
    if len(lmList) != 0:
        #Right Arm
        angle = detector.findAngle(img, 12, 14, 16, True)
        per = np.interp(angle, (180,300), (0, 100))
        bar = np.interp(angle, (180, 300), (650, 100))
        #Left Arm
        # angle_left = detector.findAngle(img, 11, 13, 15, True)
        # per_left = np.interp(angle, (50, 160), (0,100))
        # bar_left = np.interp(angle, (50, 160), (650,100))
        #print(angle, per)


        #Check for the single
        color = (255,0,255)

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

        # Check for the dumbbell curls
        # if per == 100 and per_left == 100:
        #     color = (0, 255, 0)
        #     if dir ==0:
        #         count += 0.5
        #         dir = 1
        # if per == 0 and per_left ==0
        #print(count)

        #THIS IS FOR THE BAR ON THE SIDE
        cv2.rectangle(img, (1100,100), (1175,650), color, 3)
        cv2.rectangle(img, (1100,int(bar)), (1175,650), color, cv2.FILLED)
        cv2.putText(img, f"PERCENTAGE: {str(int(per))}%", (800, 75), cv2.FONT_HERSHEY_PLAIN, 3, color, 2)

        #DRAW CURL COUNT
        #cv2.rectangle(img, (250,720), (0,0), (0,255,0), cv2.FILLED) Creates a rectangle on the left side of the video
        cv2.putText(img, f"COUNT: {str(int(count))}", (45,670), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #cv2.putText(img, f"FPS: {str(int(fps))}", (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 1)











    cv2.imshow("Live Video", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break