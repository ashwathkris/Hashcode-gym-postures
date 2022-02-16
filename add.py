import cv2
import numpy as np
import time
import PoseModule as pm
import matplotlib.pyplot as plt


import json

with open('json_data.json') as json_file:
    data = json.load(json_file)

joints = data['joints']
thresh = data['thresh']

print(joints)
print(thresh)

cap = cv2.VideoCapture("img/tryw.mp4")
#cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
#f = 50
while True:
    success, img = cap.read()
    img = cv2.resize(img, (800, 600))
    img = detector.findPose(img, False)  # remove false to see all points
    lmList = detector.findPosition(img, False)  # list of 32 points
    if len(lmList) != 0:
        for i in range(len(joints)):
            angle = detector.findAngle(img, joints[i][0], joints[i][1], joints[i][2])
            #print(angle)
            if angle < thresh[i][1] and angle > thresh[i][0]:
                print("correct posture")
            else:
            	print('Wrong posture')

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()