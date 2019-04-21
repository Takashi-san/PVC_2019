import numpy as np
import cv2 as cv
import sys

intrinsic = np.loadtxt("data/xml_files/intrinsic.xml")
distortion = np.loadtxt("data/xml_files/distortion.xml")
rotation = np.loadtxt("data/xml_files/rotation.xml")
translation = np.loadtxt("data/xml_files/translation.xml")
translation = translation.reshape((3,1))

print("=========== intrinsicos")
print(intrinsic)
print("=========== distorcao")
print(distortion)
print("=========== matriz rotacao")
print(rotation)
print("=========== vetor de translacao")
print(translation)
print("================================")

img_point = np.matrix([[0],[0],[1]])

lMat = np.linalg.inv(rotation) * np.linalg.inv(intrinsic) * img_point
rMat = np.linalg.inv(rotation) * translation

s = (translation[2,0] + rMat[2,0]/lMat[2,0])

world_point = np.linalg.inv(rotation) * (s * np.linalg.inv(intrinsic) * img_point - translation)

print(world_point)

# Callback function.
def draw_line(event, x, y, flags, param):
	global img
	global out

	if event == cv.EVENT_LBUTTONDOWN:
		draw_line.count += 1
		# Armazena ponto.
		if draw_line.count%2:
			draw_line.p1 = (x, y)

			img_point = np.matrix([[x],[y],[1]])
			lMat = np.linalg.inv(rotation) * np.linalg.inv(intrinsic) * img_point
			rMat = np.linalg.inv(rotation) * translation
			s = (translation[2,0] + rMat[2,0]/lMat[2,0])
			draw_line.p1w = np.linalg.inv(rotation) * (s * np.linalg.inv(intrinsic) * img_point - translation)
		else:
			draw_line.p2 = (x, y)

			img_point = np.matrix([[x],[y],[1]])
			lMat = np.linalg.inv(rotation) * np.linalg.inv(intrinsic) * img_point
			rMat = np.linalg.inv(rotation) * translation
			s = (translation[2,0] + rMat[2,0]/lMat[2,0])
			draw_line.p2w = np.linalg.inv(rotation) * (s * np.linalg.inv(intrinsic) * img_point - translation)
		# Desenha linha e calcula distancia.
		if draw_line.p1[0] != -1 and draw_line.p2[0] != -1:
			out = img.copy()
			cv.line(out, draw_line.p1, draw_line.p2, (0, 255, 0), 1)
			print(tcolor.GREEN + 'Distancia_pixel: ' + repr(np.linalg.norm([draw_line.p1[0] - draw_line.p2[0], draw_line.p1[1] - draw_line.p2[1]])) + tcolor.OFF)
			print(tcolor.GREEN + 'Distancia_real: ' + repr(np.linalg.norm([draw_line.p1w[0] - draw_line.p2w[0], draw_line.p1w[1] - draw_line.p2w[1]])) + tcolor.OFF)
# Variaveis estaticas.
draw_line.count = 0;
draw_line.p1 = (-1, -1)
draw_line.p2 = (-1, -1)
draw_line.p1w = np.matrix([[0],[0],[0]])
draw_line.p2w = np.matrix([[0],[0],[0]])

# Define janela e seta o evento de callback.
cv.namedWindow('image')
cv.setMouseCallback('image', draw_line)
