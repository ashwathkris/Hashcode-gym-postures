import cv2
import numpy as np
import time
import PoseModule as pm
 

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction =0 #0 if gng up, 1 if gng down
prev_per = 0
e = 0

while True:
	success, img = cap.read()
	img = cv2.resize(img, (800,600))
	#img = cv2.imread("img/test.jpg") 
	img = detector.findPose(img, False) # remove false to see all points

	lmList = detector.findPosition(img, False) #list of 32 points

	if len(lmList) != 0:
		angle = detector.findAngle(img, 11, 13, 15)
		per = np.interp(angle, (40, 170), (100, 0))
		#print(angle, per)
		##ERRORS##
		
		if direction == 0:
			if prev_per > per: 
				e+=1

			if(e == 30):
				print('Lift your arm higher')
				e= 0

		if direction == 1:
			if(prev_per < per):
				e+=1
			if(e==30):
				print('Put your arm all the way down')
				e = 0 
				
		#counting
		if per == 100: 
			if direction == 0:
				count += 0.5
				direction = 1

		if per == 0:
			if direction == 1:
				count+=0.5
				direction = 0

		prev_per = per

		cv2.putText(img, str(count), (50,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0),4)

	cv2.imshow("Image", img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()