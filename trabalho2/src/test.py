import cv2 as cv
import numpy as np

intrinsic = np.loadtxt("xml_files/intrisics.xml")
distortion = np.loadtxt("xml_files/distortion.xml")

print(intrinsic)
print(distortion)

ret, rot_vec, trans_vec = cv.solvePnP()



img = cv.imread("cam_notebook/notebook30.jpg")
h,  w = img.shape[:2]
newcameramtx, roi=cv.getOptimalNewCameraMatrix(intrinsic, distortion, (w,h), 1, (w,h))
undist = cv.undistort(img, intrinsic, distortion, None, newcameramtx)

while True:
	cv.imshow('undist', undist)
	cv.imshow('raw', img)
	a = cv.waitKey(1)
	if a == 27:
		break
