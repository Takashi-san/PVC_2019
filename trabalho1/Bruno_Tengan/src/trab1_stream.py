import numpy as np
import cv2 as cv
import sys

# ANSI escape sequences.
class tcolor:
    MAGENTA = '\033[95m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    WHITE = '\033[37;1m'
    OFF = '\033[0m'

# Color reference init.
b = 500
g = 500
r = 500

# Open webcam(try only the first available).
cap = cv.VideoCapture(0)
if cap.isOpened() is False:
	cap.open(0)
	if cap.isOpened() is False:
		print(tcolor.RED + 'Failed to access webcam.' + tcolor.OFF)
		raise SystemExit

# Mouse callback function
def get_frame_info(event, x, y, flags, param):
	global frame
	global out
	global b, g, r

	if event == cv.EVENT_LBUTTONDOWN:
		# Print frame pixel info.
		print(tcolor.YELLOW + '-------------------------------------')
		print(tcolor.MAGENTA + 'Row: ' + repr(y) + ' Column: ' + repr(x))
		b, g, r = frame[y, x]
		print(tcolor.RED + 'r= ' + repr(r) + tcolor.GREEN + ' g= ' + repr(g) + tcolor.BLUE + ' b= ' + repr(b) + tcolor.OFF)	

# Create window and bind the function to window.
cv.namedWindow('frame')
cv.setMouseCallback('frame', get_frame_info)
print(tcolor.YELLOW + 'Press ESC to exit.' + tcolor.OFF)

# Main loop.
while(cap.isOpened()):
	ret, frame = cap.read()
	
	# Highlight similar pixels.
	out = frame.copy()
	ref = np.array([b, g, r])
	test = frame.astype(int) - ref
	test = test**2
	test = test.sum(axis=2)
	test = test**0.5
	out[test<13] = [0, 0, 255]

	cv.imshow('frame', out)
	a = cv.waitKey(1)
	if a == 27:
		break

cap.release()
cv.destroyAllWindows()