import cv2
import numpy as np
import time
import PoseModule as pm
import matplotlib.pyplot as plt
import mediapipe as mp
mp_pose = mp.solutions.pose
import json

n = int(input('Enter number of joints needed: '))
mainlist = []
allang=[]
for i in range(n):
	listofjoins = []
	print('Enter Joint ', i+1 , ':')
	for j in range(3):
		listofjoins.append(int(input()))
	mainlist.append(listofjoins)
	allang.append([])
print(mainlist)

img = cv2.imread("img/wallsit.jpg")
detector = pm.poseDetector()
img = cv2.resize(img, (800, 600))
img = detector.findPose(img, False)  # remove false to see all points
lmList = detector.findPosition(img, False)  # list of 32 points
if len(lmList) != 0:
	for i in  range(len(mainlist)):
		angle = detector.findAngle(img, mainlist[i][0], mainlist[i][1], mainlist[i][2])
		allang[i].append(angle)


thresh=[[max(0,min(i)-20),min(180, max(i)+20)] for i in allang]
print(allang[0])
print(thresh)

data={
    'joints':mainlist,
    'thresh':thresh
}

# json_string = json.dumps(data)

with open('json_data.json', 'w') as outfile:
    json.dump(data, outfile)

cv2.destroyAllWindows()