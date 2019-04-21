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

# Busca argumentos.
if len(sys.argv) != 2:
	print(tcolor.RED + 'Wrong argument. Python3 trab2_req4.py path_img_to_measure' + tcolor.OFF)
	raise SystemExit	#sys.exit
test = str(sys.argv[1])

# Criterios para refinamento dos pontos.
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepara os pontos de objeto na escala do quadrado do xadrez.
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7*3:3,0:6*3:3].T.reshape(-1,2)

# Arrays para guardar os pontos do objeto e pontos da imagem.
objpoints = [] # Pontos no mundo real em 3D.
imgpoints = [] # Pontos na imagem em 2D.

# Carrega arquivos xml com as informacoes dos intrinsecos e distorcao da camera.
intrinsic = np.loadtxt("data/xml_files/intrinsic.xml")
distortion = np.loadtxt("data/xml_files/distortion.xml")

print(tcolor.YELLOW + "=========== intrinsecos" + tcolor.OFF)
print(intrinsic)
print(tcolor.YELLOW + "=========== distorcao" + tcolor.OFF)
print(distortion)
print(tcolor.YELLOW + "================================" + tcolor.OFF)

while(1):
	img = cv.imread(test)

	# Converte imagem para escala de cinza
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Identifica o padrao de xadrez 7x6.
	ret, corners = cv.findChessboardCorners(gray, (7,6), None)

    # Obtem os pontos do objeto e imagem se reconhecer o padrao.
	if ret == True:
		# Aumenta a acuracia dos pontos encontrados.
		corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)

        # Desenha e mostra os pontos encontrados.
		img = cv.drawChessboardCorners(img, (7,6), corners2, ret)
		cv.imshow('Snapshot ', img)
		cv.waitKey(500)
		break

print("*** Obtido os snapshots. ***")
print(tcolor.YELLOW + "APERTE QUALQUER TECLA" + tcolor.OFF)

cv.waitKey(0)
cv.destroyAllWindows()

ret, rotation, translation = cv.solvePnP(objp, corners2, intrinsic, distortion)
rotation, jacob = cv.Rodrigues(rotation)

# Retira a distorcao da imagem.
img = cv.imread(test)
h,  w = img.shape[:2]
newcameramtx, roi=cv.getOptimalNewCameraMatrix(intrinsic, distortion, (w,h), 1, (w,h))
img = cv.undistort(img, intrinsic, distortion, None, newcameramtx)

# Callback function.
def draw_line(event, x, y, flags, param):
	global img
	global out

	if event == cv.EVENT_LBUTTONDOWN:
		draw_line.count += 1
		# Armazena ponto na imagem e sua posicao no munodo real.
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
		
		# Desenha linha e calcula distancias.
		if draw_line.p1[0] != -1 and draw_line.p2[0] != -1:
			out = img.copy()
			cv.line(out, draw_line.p1, draw_line.p2, (0, 255, 0), 1)
			print(tcolor.MAGENTA + 'Distancia_pixel: ' + repr(np.linalg.norm([draw_line.p1[0] - draw_line.p2[0], draw_line.p1[1] - draw_line.p2[1]])) + tcolor.OFF)
			print(tcolor.BLUE + 'Distancia_real: ' + repr(np.linalg.norm([draw_line.p1w[0,0] - draw_line.p2w[0,0], draw_line.p1w[1,0] - draw_line.p2w[1,0], draw_line.p1w[2,0] - draw_line.p2w[2,0]])) + ' cm' + tcolor.OFF)
# Variaveis estaticas.
draw_line.count = 0;
draw_line.p1 = (-1, -1)
draw_line.p2 = (-1, -1)
draw_line.p1w = np.matrix([[0],[0],[0]])
draw_line.p2w = np.matrix([[0],[0],[0]])

# Define janela e seta o evento de callback.
cv.namedWindow('undist')
cv.setMouseCallback('undist', draw_line)

out = img.copy()
print(tcolor.YELLOW + "APERTE ESC PARA SAIR" + tcolor.OFF)
while True:
	cv.imshow('image', out)
	a = cv.waitKey(1)
	if a == 27:
		break
