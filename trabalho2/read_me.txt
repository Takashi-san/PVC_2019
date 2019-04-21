Aluno: Bruno Takashi Tengan
Matrícula: 12/0167263

Programas desenvolvidos no ambiente:
OS: Linux Ubuntu 16.04
Python: Python 3.5.2
OpenCV: OpenCV 3.3.1-dev

Argumentos de execução:
Requisito1--------------------------
trab2_req1.py
	# Executa sem argumento. 
	# Simplesmente desenha em uma imagem preta.

Requisito2--------------------------
trab2_req2.py diretorio_com_snapshots caminho_foto_para_corrigir_distorcao
	# Executa com um diretório e uma imagem.
	# Analisa todos .jpg no diretório e busca os padrões de calibração.
	# Depois de calibrado tira distorção da imagem fornecido e permite medir distância em pixel entre o raw e o undistort.

Requisito3--------------------------
trab2_req3.py diretorio_com_snapshots
	# Executa com um diretório.
	# Tenta achar 3 .jpg que tenha o padrão de calibração.
	# Utiliza os arquivos .xml dos intrínsecos.
	# Retorna a média |t| e o desvio padrão entre as 3 imagens.

Requisito4--------------------------
trab2_req4.py caminho_imagem_para_medir
	# Executa com uma imagem.
	# Ele calibra o extrínseco pelo padrão de calibração presente na imagem, se não achar fica em loop infinito.
	# Se quiser colocar uma imagem específica para calibrar o extrínseco mude a linha 43 substituindo "test" pela imagem que quer.
	# Permite medir distância em pixel da imagem e distância real em cm.
