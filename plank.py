import cv2
import numpy as np
import time
import PoseModule as pm
import matplotlib.pyplot as plt 
import random

#cap = cv2.VideoCapture("img/plank2.mp4")
cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
e1 = 0
e2=0
e22=0
e3=0

l1 = []
l2 = []
start = time.time()

while True:
	success, img = cap.read()
	img = cv2.resize(img, (800,600))
	#img = cv2.imread("img/plank.jpg")
	img = detector.findPose(img,False) # remove false to see all points
	
	lmList = detector.findPosition(img, False) #list of 32 points

	if len(lmList) != 0:
		angle1 = detector.findAngle(img, 11, 13, 15)#	elbow
		angle2 = detector.findAngle(img, 11, 23, 25)#   hip
		angle3 = detector.findAngle(img, 23, 25, 27)#	legs

		l1.append(angle1)
		l2.append(angle2)

		#x`print(angle1, angle2, angle3)
		if not 75<=angle1<=105:
			e1+=1
		if(e1==40):
			print('Bring your shoulder vertically above your elbow')
			e1 = 0

		if angle2<140:
			e2+=1
		if(e2==40):
			print('Make your back straight. Bring your buttocks DOWN')
			e2 = 0 

		if angle2 > 170:
			e22+=1
		if(e22==40):
			print('Make your back straight. Bring your buttocks UP')
			e2=0


		if angle3<=160 :
			e3+=1
		if(e3==40):
			print('Do not bend your knee. Stretch your legs')
			e3 = 0


		#cv2.putText(img, str(count), (50,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0),4)

	cv2.imshow("Image", img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

'''
x = [i for i in range(len(l1))]
plt.plot(x, l1, label = 'line1')
plt.plot(x, l2, label = 'line2')
plt.xlabel("Time")
plt.ylabel("Accuracy")
plt.axhline(y = elb, color = 'g', linestyle = '-', label = "Ideal position of the elbow")
plt.axhline(y = back, color = 'r', linestyle = '-', label = "Ideal position of the back")
plt.legend(fontsize = 5)
plt.show()
'''


#############GRAPH##############
# Placing the plots in the plane

end = time.time()
duration = end - start
d = len(l1)//duration
plot1 = plt.subplot2grid((1, 2), (0, 0), colspan=1)
plot2 = plt.subplot2grid((1, 2), (0, 1), colspan=1)
  
# Using Numpy to create an array x
x = [i/d for i in range(len(l1))] 

plot2.plot(x, l1)
plot2.set_xlabel("Time")
plot2.set_ylabel("Accuracy")
plot2.axhline(y = 80, color = 'g', linestyle = '-', label = "Ideal position of the elbow")
plot2.set_title('Accuracy of the Elbow')

plot1.plot(x, l2)
plot1.set_xlabel("Time")
plot1.set_ylabel("Accuracy")
plot1.axhline(y = 160, color = 'r', linestyle = '-', label = "Ideal position of the elbow")
plot1.set_title('Accuracy of the Back')

plt.show()