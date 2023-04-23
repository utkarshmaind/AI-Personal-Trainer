import cv2
import numpy as np
import time
import posemodule as pm

cap = cv2.VideoCapture(0)

detector = pm.poseDetector()
count1 = 0
count2 = 0
dir1 = 0
dir2 = 0
pTime = 0
stage = None
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1920, 1080))
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        # Right Arm
        angle1 = detector.findAngle(img, 12, 14, 16)
        # # Left Arm
        angle2 = detector.findAngle(img, 11, 13, 15)
        per1 = np.interp(angle1, (210, 310), (0, 100))
        per2 = np.interp(angle2, (210, 310), (0, 100))
        bar1 = np.interp(angle1, (220, 310), (650, 100))
        bar2 = np.interp(angle2, (220, 310), (650, 100))
        # print(angle, per)

        # Check for the dumbbell curls
        color1 = (0, 0, 255)
        if per1 == 100:
            color1 = (0, 255, 0)
            if dir1 == 0:
                count1 += 0.5
                dir1 = 1
        if per1 == 0:
            color1 = (1, 190, 200)
            if dir1 == 1:
                count1 += 0.5
                dir1 = 0
        print(count1)

        # Check for the dumbbell curls
        color2 = (0, 0, 255)
        if per2 == 100:
            color2 = (0, 255, 0)
            if dir2 == 0:
                count2 += 0.5
                dir2 = 1
        if per2 == 0:
            color2 = (1, 190, 200)
            if dir2 == 1:
                count2 += 0.5
                dir2 = 0
        print(count2)

        # Draw Bar right
        cv2.rectangle(img, (1380, 100), (1450, 650), color2, 3)
        cv2.rectangle(img, (1380, int(bar2)), (1450, 650), color2, cv2.FILLED)
        cv2.putText(img, f'{int(per2)}%', (1360, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color2, 4)
        # Draw Bar left
        cv2.rectangle(img, (80, 100), (150, 650), color1, 3)
        cv2.rectangle(img, (80, int(bar1)), (150, 650), color1, cv2.FILLED)
        cv2.putText(img, f'{int(per1)}%', (80, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color1, 4)

        # Draw Curl Count right
        cv2.rectangle(img, (1400, 810), (1505, 740), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count2)), (1400, 800), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 10)

        # Draw Curl Count left
        cv2.rectangle(img, (50, 810), (155, 740), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count1)), (50, 800), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 10)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                #(255, 0, 0), 5)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

