import numpy as np
import cv2 as cv
import glob

# Criterios para refinamento dos pontos.
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepara os pontos de objeto na escala do quadrado do xadrez.
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays para guardar os pontos do objeto e pontos da imagem.
objpoints = [] # Pontos no mundo real em 3D.
imgpoints = [] # Pontos na imagem em 2D.

count = 5
valid = True
cap = cv.VideoCapture(0)

print("*** Obtendo os snapshots. ***")
# Quantidade de snapshots a capturar.
while(1):
	try:
		ret, frame = cap.read()
		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	except:
		valid = False

	if valid:
		# Converte imagem para escala de cinza

	    # Identifica o padrao de xadrez 7x6.
		ret, corners = cv.findChessboardCorners(gray, (7,6), None)

	    # Obtem os pontos do objeto e imagem se reconhecer o padrao.
		if ret == True:
			# Aumenta a acuracia dos pontos encontrados.
			corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)

	        # Desenha e mostra os pontos encontrados.
			gray = cv.drawChessboardCorners(gray, (7,6), corners2, ret)
	valid = True			

	# Mostra imagem original.
	cv.imshow('ori', gray)
	a = cv.waitKey(1)
	if a == 27:
		break
	if a == 32:
		count += 1
		cv.imwrite("data/object/notebook_object" + repr(count) + ".jpg", frame)
		print("saved!!!!!!!!!!!!!!!!!!!!!!!")
# FIM WHILE OBTER OS SNAPSHOTS =================================================================
cap.release()