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
if len(sys.argv) != 2:
	print(tcolor.RED + 'Wrong argument. Python3 trab2_req3.py path_img_dir' + tcolor.OFF)
	raise SystemExit	#sys.exit
source = str(sys.argv[1])

# Criterios para refinamento dos pontos.
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepara os pontos de objeto na escala do quadrado do xadrez.
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7*3:3,0:6*3:3].T.reshape(-1,2)

# Arrays para guardar os pontos do objeto e pontos da imagem.
objpoints = [] # Pontos no mundo real em 3D.
imgpoints = [] # Pontos na imagem em 2D.

# Carrega intrinsecos.
intrinsic = np.loadtxt("data/xml_files/intrinsic.xml")
distortion = np.loadtxt("data/xml_files/distortion.xml")

images = glob.glob(source + '*.jpg')
i = 0
count = 0;
dist = np.zeros(3)
for fname in images:
#while(1):
	img = cv.imread(fname)

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

		# Pega as distâncias das 3 primeiras imagens.
		ret, rot_vec, trans_vec = cv.solvePnP(objp, corners2, intrinsic, distortion)
		dist[count] = np.linalg.norm([trans_vec[0,0], trans_vec[1,0], trans_vec[2,0]])
		if count == 2:
			break			
		count += 1

# FIM WHILE OBTER OS SNAPSHOTS =================================================================

print("*** Obtido os snapshots. ***")
print(tcolor.YELLOW + "APERTE QUALQUER TECLA" + tcolor.OFF)

cv.waitKey(0)
cv.destroyAllWindows()

m_dist = np.sum(dist)/3
print(tcolor.YELLOW + "=========== distancia media" + tcolor.OFF)
print(repr(m_dist))
dp_dist = (np.sum(np.square(dist - m_dist))/3)**(1/2)
print(tcolor.YELLOW + "=========== desvio padrao" + tcolor.OFF)
print(repr(dp_dist))
'''
print("*** Calibrando. ***")
ret, rot_vec, trans_vec = cv.solvePnP(objp, corners2, intrinsic, distortion)
print("*** Calibrado. ***")
print("=========== rotation matrix")
matr, jacob = cv.Rodrigues(rot_vec)
print(matr)
print("=========== translation vector")
print(trans_vec)
'''
'''
print("*** Salvando arquivos intrisics.xml e distortion.xml. ***")
np.savetxt('data/xml_files/rotation.xml', matr)
np.savetxt('data/xml_files/translation.xml', trans_vec)
print("*** Arquivos salvos. ***")
'''