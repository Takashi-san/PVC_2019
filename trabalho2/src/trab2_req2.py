import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

count = 0
valid = True
cap = cv2.VideoCapture(0)

while(1):
	#try:
	ret, img = cap.read()

	'''
	except:
		print("error take image.")
		valid = False
	'''

	cv2.imshow('ori', img)
	a = cv2.waitKey(15)
	
	if a == 27:
		if count > 5: 
			cap.release()
			break
	

	#if valid == True and count != 5:	
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Identifica o padrao de xadrez 7x6.
	ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

    # If found, add object points, image points (after refining them)
	if ret == True:
		objpoints.append(objp)

		# Aumenta a acuracia dos pontos encontrados.
		corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		imgpoints.append(corners2)

        # Desenha e mostra os pontos encontrados.
		img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
		cv2.imshow('snapshot ',img)
		count += 1
	#valid = True			

cap.release()
cv2.destroyAllWindows()