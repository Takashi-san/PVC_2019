import numpy as np
import cv2 as cv
import glob
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
if len(sys.argv) != 3:
	print(tcolor.RED + 'Wrong argument. Python3 trab2_req2.py path_snapshots_dir path_img_to_undistort' + tcolor.OFF)
	raise SystemExit	#sys.exit
source = str(sys.argv[1])
test = str(sys.argv[2])

# Criterios para refinamento dos pontos.
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepara os pontos de objeto na escala do quadrado do xadrez.
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays para guardar os pontos do objeto e pontos da imagem.
objpoints = [] # Pontos no mundo real em 3D.
imgpoints = [] # Pontos na imagem em 2D.

images = glob.glob(source + '*.jpg')

for fname in images:
	img = cv.imread(fname)

	# Converte imagem para escala de cinza
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Identifica o padrao de xadrez 7x6.
	ret, corners = cv.findChessboardCorners(gray, (7,6), None)

    # Obtem os pontos do objeto e imagem se reconhecer o padrao.
	if ret == True:
		objpoints.append(objp)

		# Aumenta a acuracia dos pontos encontrados.
		corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
		imgpoints.append(corners2)

        # Desenha e mostra os pontos encontrados.
		img = cv.drawChessboardCorners(img, (7,6), corners2, ret)
		cv.imshow('Snapshot ', img)
		cv.waitKey(500)			

# FIM WHILE OBTER OS SNAPSHOTS =================================================================

print("*** Obtido os snapshots. ***")
print(tcolor.YELLOW + "APERTE QUALQUER TECLA" + tcolor.OFF)

cv.waitKey(0)
cv.destroyAllWindows()

print("*** Calibrando. ***")

ret_val, intri_mtx, dist_coef, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

print("*** Calibrado. ***")
print("*** Salvando arquivos intrisics.xml e distortion.xml. ***")

np.savetxt('data/xml_files/intrinsic.xml', intri_mtx)
np.savetxt('data/xml_files/distortion.xml', dist_coef)

print("*** Arquivos salvos. ***")

img = cv.imread(test)
h,  w = img.shape[:2]
newcameramtx, roi=cv.getOptimalNewCameraMatrix(intri_mtx, dist_coef, (w,h), 1, (w,h))
undist = cv.undistort(img, intri_mtx, dist_coef, None, newcameramtx)

# Callback function.
def draw_line_undist(event, x, y, flags, param):
	global undist
	global out1

	if event == cv.EVENT_LBUTTONDOWN:
		draw_line_undist.count += 1
		# Armazena ponto.
		if draw_line_undist.count%2:
			draw_line_undist.p1 = (x, y)
		else:
			draw_line_undist.p2 = (x, y)
		# Desenha linha e calcula distancia.
		if draw_line_undist.p1[0] != -1 and draw_line_undist.p2[0] != -1:
			out1 = undist.copy()
			cv.line(out1, draw_line_undist.p1, draw_line_undist.p2, (0, 0, 255), 1)
			print(tcolor.RED + 'Distancia_undist: ' + repr(np.linalg.norm([draw_line_undist.p1[0] - draw_line_undist.p2[0], draw_line_undist.p1[1] - draw_line_undist.p2[1]])) + tcolor.OFF)
# Variaveis estaticas.
draw_line_undist.count = 0;
draw_line_undist.p1 = (-1, -1)
draw_line_undist.p2 = (-1, -1)

# Callback function.
def draw_line_raw(event, x, y, flags, param):
	global img
	global out2

	if event == cv.EVENT_LBUTTONDOWN:
		draw_line_raw.count += 1
		# Armazena ponto.
		if draw_line_raw.count%2:
			draw_line_raw.p1 = (x, y)
		else:
			draw_line_raw.p2 = (x, y)
		# Desenha linha e calcula distancia.
		if draw_line_raw.p1[0] != -1 and draw_line_raw.p2[0] != -1:
			out2 = img.copy()
			cv.line(out2, draw_line_raw.p1, draw_line_raw.p2, (0, 255, 0), 1)
			print(tcolor.GREEN + 'Distancia_raw: ' + repr(np.linalg.norm([draw_line_raw.p1[0] - draw_line_raw.p2[0], draw_line_raw.p1[1] - draw_line_raw.p2[1]])) + tcolor.OFF)
# Variaveis estaticas.
draw_line_raw.count = 0;
draw_line_raw.p1 = (-1, -1)
draw_line_raw.p2 = (-1, -1)

# Define janela e seta o evento de callback.
cv.namedWindow('raw')
cv.setMouseCallback('raw', draw_line_raw, img)
cv.namedWindow('undist')
cv.setMouseCallback('undist', draw_line_undist, undist)

out2 = img.copy()
out1 = undist.copy()
print(tcolor.YELLOW + "APERTE ESC PARA SAIR" + tcolor.OFF)
while True:
	cv.imshow('undist', out1)
	cv.imshow('raw', out2)
	a = cv.waitKey(1)
	if a == 27:
		break
