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
l = 500

# Video path from arguments.
if len(sys.argv) != 2:
	print(tcolor.RED + 'Missing argument. Python trab1_video.py video_name/path' + tcolor.OFF)
	raise SystemExit	#sys.exit
source = str(sys.argv[1])

# Check if the video is gray scale or color.
def is_gray():
	test = cv.VideoCapture(source)
	if test.isOpened() is False:
		print(tcolor.RED + 'Failed to load video.' + tcolor.OFF)
		raise SystemExit
	while test.isOpened():
		ret, frame = test.read()
		b = frame[:,:,0]
		g = frame[:,:,1]
		r = frame[:,:,2]
		if np.any((b == g) == 0):
			return False
		if np.any((g == r) == 0):
			return False
	return True


# Mouse callback function
def get_frame_info(event, x, y, flags, param):
	global frame
	global out
	global b, g, r, l

	if event == cv.EVENT_LBUTTONDOWN:
		# Print frame pixel info.
		if cflag:
			# GRAY.
			print(tcolor.YELLOW + '-------------------------------------')
			print(tcolor.MAGENTA + 'Row: ' + repr(y) + ' Column: ' + repr(x))
			l = frame[y, x]
			print(tcolor.WHITE + 'Intensity: ' + repr(l) + tcolor.OFF)
		else:
			# BGR.
			print(tcolor.YELLOW + '-------------------------------------')
			print(tcolor.MAGENTA + 'Row: ' + repr(y) + ' Column: ' + repr(x))
			b, g, r = frame[y, x]
			print(tcolor.RED + 'r= ' + repr(r) + tcolor.GREEN + ' g= ' + repr(g) + tcolor.BLUE + ' b= ' + repr(b) + tcolor.OFF)	
		
# Create window and bind the function to window.
cv.namedWindow('frame')
cv.setMouseCallback('frame', get_frame_info)
print(tcolor.YELLOW + 'Press ESC to exit.' + tcolor.OFF)

if is_gray():
	cflag = 1
else:
	cflag = 0
cap = cv.VideoCapture(source)
if cap.isOpened() is False:
	print(tcolor.RED + 'Failed to load video.' + tcolor.OFF)
	raise SystemExit

# Main loop.
while(cap.isOpened()):
	ret, frame = cap.read()
	
	# Highlight similar pixels.
	if cflag:
		out = frame.copy()
		frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		test = np.absolute(frame.astype(int) - l)
		out[test<13] = [0, 0, 255]
	else:
		out = frame.copy()
		ref = np.array([b, g, r])
		test = frame.astype(int) - ref
		test = test**2
		test = test.sum(axis=2)
		test = test**0.5
		out[test<13] = [0, 0, 255]

	cv.imshow('frame', out)
	a = cv.waitKey(33) # Frame rate de 30FPS.
	if a == 27:
		break

cap.release()
cv.destroyAllWindows()