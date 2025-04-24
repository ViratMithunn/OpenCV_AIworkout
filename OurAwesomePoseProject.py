import cv2
import time
import PoseModule as pm


cap = cv2.VideoCapture("PoseVideos/IMG_2634.MOV")
pTime = 0
detector = pm.poseDetector()

while True:
    success, img = cap.read()
    #img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE) #THIS LINE OF CODE IS OPTIONAL TO ROTATE
    if not success:
        break

    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) > 32:
        print(lmList[14])
        cv2.circle(img, (lmList[14][1], lmList[14][2]), 10, (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()