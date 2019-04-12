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

# Image path from arguments.
if len(sys.argv) != 2:
	print(tcolor.RED + 'Missing argument. Python trab1_img.py img_name/path' + tcolor.OFF)
	raise SystemExit	#sys.exit
source = str(sys.argv[1])

# Show List of events.
#events = [i for i in dir(cv) if 'EVENT' in i]
#print( events )

# Check if the image is gray scale or color.
def is_gray():
	test = cv.imread(source)
	if test is None:
		print(tcolor.RED + 'Failed to load image.' + tcolor.OFF)
		raise SystemExit
	b = test[:,:,0]
	g = test[:,:,1]
	r = test[:,:,2]
	if np.any((b == g) == 0):
		return False
	if np.any((g == r) == 0):
		return False
	return True

# Mouse callback function
def get_img_info(event, x, y, flags, param):
	global img
	global out
	global cflag

	if event == cv.EVENT_LBUTTONDOWN:
		if cflag :
			# BGR.
			# Print image pixel info.
			print(tcolor.YELLOW + '-------------------------------------')
			print(tcolor.MAGENTA + 'Row: ' + repr(y) + ' Column: ' + repr(x))
			b, g, r = img[y, x]
			print(tcolor.RED + 'r= ' + repr(r) + tcolor.GREEN + ' g= ' + repr(g) + tcolor.BLUE + ' b= ' + repr(b) + tcolor.OFF)
			
			# Highlight similar pixels.
			out = img.copy()
			ref = np.array([b, g, r])
			test = img.astype(int) - ref
			test = test**2
			test = test.sum(axis=2)
			test = test**0.5
			out[test<13] = [0, 0, 255]

		else:
			# GRAY.
			# Print image pixel info.
			print(tcolor.YELLOW + '-------------------------------------')
			print(tcolor.MAGENTA + 'Row: ' + repr(y) + ' Column: ' + repr(x))
			l = img[y, x]
			print(tcolor.WHITE + 'Intensity: ' + repr(l) + tcolor.OFF)
			
			# Highlight similar pixels.
			out = img.copy()
			out = cv.cvtColor(out, cv.COLOR_GRAY2BGR)
			test = np.absolute(img.astype(int) - l)
			out[test<13] = [0, 0, 255]

# Load image.
if is_gray():
	cflag = 0
	img = cv.imread(source, cv.IMREAD_GRAYSCALE)
	out = cv.imread(source)
else:
	cflag = 1
	img = cv.imread(source)
	out = img.copy()

# Create window and bind the function to window.
cv.namedWindow('image')
cv.setMouseCallback('image', get_img_info)
print(tcolor.YELLOW + 'Press ESC to exit.' + tcolor.OFF)

# Main loop.
while(1):
	cv.imshow('image', out)
	a = cv.waitKey(1)
	if a == 27:
		break
cv.destroyAllWindows()