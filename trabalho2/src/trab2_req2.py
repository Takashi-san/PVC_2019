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

count = 0
valid = True
cap = cv.VideoCapture(0)

print("*** Obtendo os snapshots. ***")
#while(1):
while(count < 50):
	try:
		ret, frame = cap.read()

	except:
		valid = False

	if valid:
		# Converte imagem para escala de cinza
		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	    # Identifica o padrao de xadrez 7x6.
		ret, corners = cv.findChessboardCorners(gray, (7,6), None)

	    # Obtem os pontos do objeto e imagem se reconhecer o padrao.
		if ret == True:
			objpoints.append(objp)

			# Aumenta a acuracia dos pontos encontrados.
			corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
			imgpoints.append(corners2)

	        # Desenha e mostra os pontos encontrados.
			frame = cv.drawChessboardCorners(frame, (7,6), corners2, ret)
			cv.imshow('Snapshot ', frame)
			cv.waitKey(1)
			count += 1
	valid = True			

	'''
	# Mostra imagem original.
	cv.imshow('ori', frame)
	a = cv.waitKey(15)
	if a == 27:
		if count > 5: 
			cap.release()
			break
	'''
# FIM WHILE OBTER OS SNAPSHOTS =================================================================

print("*** Obtido os snapshots. ***")
print("APERTE QUALQUER TECLA")

cv.waitKey(0)
cv.destroyAllWindows()

print("*** Calibrando. ***")

ret_val, intri_mtx, dist_coef, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

print("*** Calibrado. ***")
print("*** Salvando arquivos intrisics.xml e distortion.xml. ***")

np.savetxt('intrisics.xml', intri_mtx)
np.savetxt('distortion.xml', dist_coef)

print("*** Arquivos salvos. ***")

h, w = gray.shape[::-1]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(intri_mtx, dist_coef, (w,h), 1, (w,h))

print("APERTE ESC PARA SAIR")
while True:
	ret, frame = cap.read()

	undist = cv.undistort(frame, intri_mtx, dist_coef, None, newcameramtx)

	#x, y, w, h = roi
	#undist = undist[y:y+h, x:x+w]

	cv.imshow('undist', undist)
	cv.imshow('raw', frame)
	a = cv.waitKey(1)
	if a == 27:
		break
