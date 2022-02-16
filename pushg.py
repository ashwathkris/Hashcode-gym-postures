import cv2
import numpy as np
import time
import PoseModule as pm
import matplotlib.pyplot as plt


#cap = cv2.VideoCapture("The Push-Up_Trim.mp4")
cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0  # 0 if gng down, 1 if gng up
prev_per = 0
e = 0

l1 = []
l2 = []
err_top=[]
err_bottom=[]
d = 0
start=time.time()
while True:
	success, img = cap.read()
	img = cv2.resize(img, (800, 600))
	img = detector.findPose(img, False)  # remove false to see all points

	lmList = detector.findPosition(img, False)  # list of 32 points

	if len(lmList) != 0:
		elbowAngle = detector.findAngle(img, 12, 14, 16)
		buttAngle = detector.findAngle(img, 12, 24, 26)
		legAngle = detector.findAngle(img, 24, 26, 28)
		#elbowAngle = detector.findAngle(img, 11, 13, 15)
		#buttAngle = detector.findAngle(img, 11, 23, 25)
		#legAngle = detector.findAngle(img, 23, 25, 27)

		per = np.interp(elbowAngle, (80, 160), (100, 0))
		# print(angle, per)
		##ERRORS##
		if direction == 0:
			# elbow>165
            # but>160
            # leg>170
			if legAngle<160:
				d+=1
			if(d==40):
				print('make your legs straighter')
				cv2.putText(img, "make your legs straighter", (0,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),4)
				d=0
			if buttAngle<155:
				d+=1
				#cv2.putText(img, "make your butt straighter", (0,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),4)
			if(d==40):
					print('make your back straight.')  
					cv2.putText(img, "make your back straight.", (0,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),4)
					d=0        
			
			if prev_per > per: 
				e+=1

			if(e == 40):
				print('bring your chest closer to the ground!')
				e= 0
				
		if direction == 1:#going up
			# elbow<40
            # but>160
            # leg>170
			if legAngle<160:
				d+=1
			if(d==40):
				cv2.putText(img, "make your legs straighter", (0,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),4)
				print('make your legs straighter')
				d=0
			if buttAngle<155:
				d+=1
			if(d==40):
				cv2.putText(img, "Make your back straight", (0,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),4)
				print('make your back straight.')  
				d=0        

			if(prev_per > per):
				e+=1
			if(e==40):
				print('Higher! Straighten your hands')
				e= 0
                	
		# counting
		if elbowAngle <= 70: 
			if direction == 0:
				count += 0.5
				err_bottom.append(elbowAngle)
				direction = 1

		if elbowAngle >= 165:
			if direction == 1:
				count+=0.5
				err_top.append(elbowAngle)
				direction = 0

		prev_Angle = elbowAngle
		cv2.putText(img, str(count), (50,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0),4)

	cv2.imshow("Image", img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
            break

end=time.time()
duration=end-start

top=np.array(err_top)
bottom=np.array(err_bottom)
d=len(top)//duration

x=np.array([i for i in range(max(len(err_top),len(err_bottom)))])

plt1=plt.subplot2grid((1,2),(0,0),colspan=1)
plt2=plt.subplot2grid((1,2),(0,1),colspan=1)

plt1.axhline(y = 167, color = 'r', linestyle = 'dashed',label = "ideal position at the top")
plt2.axhline(y = 69, color = 'g', linestyle = 'dashed',label = "ideal position at the bottom")
plt1.plot(np.array([i/40 for i in range(len(err_top))]),top,color="blue",linewidth = 1,label = "user position at the top")
plt2.plot(np.array([i/40 for i in range(len(err_bottom))]),bottom,color="yellow",linewidth = 1, label = "user position at the top")
plt1.set_ylim(100,200)
plt2.set_ylim(50,100)

plt1.set_xlabel('time')
plt2.set_xlabel('time')

# naming the y axis
plt1.set_ylabel('accuracy')
plt2.set_ylabel('accuracy')

plt1.set_title('Accuracy of position(top)')
plt2.set_title('Accuracy of position(bottom)')


plt1.legend()
plt2.legend()
plt.show()

cap.release()
cv2.destroyAllWindows()