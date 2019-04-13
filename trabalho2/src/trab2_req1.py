import numpy as np
import cv2 as cv

# ANSI escape sequences.
class tcolor:
    MAGENTA = '\033[95m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    WHITE = '\033[37;1m'
    OFF = '\033[0m'

# Cria imagem preta.
img = np.zeros((600, 600, 3), np.uint8)

# Callback function.
def draw_line(event, x, y, flags, param):
	global img
	global out

	if event == cv.EVENT_LBUTTONDOWN:
		draw_line.count += 1
		# Armazena ponto.
		if draw_line.count%2:
			draw_line.p1 = (x, y)
		else:
			draw_line.p2 = (x, y)
		# Desenha linha e calcula distancia.
		if draw_line.p1[0] != -1 and draw_line.p2[0] != -1:
			out = img.copy()
			cv.line(out, draw_line.p1, draw_line.p2, (0, 0, 255), 1)
			print(tcolor.WHITE + 'Distancia: ' + repr(np.linalg.norm([draw_line.p1[0] - draw_line.p2[0], draw_line.p1[1] - draw_line.p2[1]])) + tcolor.OFF)
# Variaveis estaticas.
draw_line.count = 0;
draw_line.p1 = (-1, -1)
draw_line.p2 = (-1, -1)

# Define janela e seta o evento de callback.
cv.namedWindow('image')
cv.setMouseCallback('image', draw_line)

# Main loop.
out = img.copy()
print(tcolor.YELLOW + 'Press ESC to exit.' + tcolor.OFF)
while(1):
	cv.imshow('image', out)
	a = cv.waitKey(1)
	if a == 27:
		break
cv.destroyAllWindows()