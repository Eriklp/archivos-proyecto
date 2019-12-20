from argparse import ArgumentParser
import sys

parser = ArgumentParser(description='%(prog)s cortadorSequencia')

parser.add_argument('archivo', help ='ruta del fichero de c elegans que sera cortada')

args = parser.parse_args()

nombreArchivo = args.archivo

print(nombreArchivo)

with open(nombreArchivo, "r") as archivo:
	lineas = archivo.readlines()
	j = 1
	secuencia = ""
	for i in  range(0, len(lineas)):
		if i >= 1031928 and i < 1253416:
			secuencia += lineas[i]
			#print(lineas[i])
	print(secuencia)
	archivoGuardar = open("Caenorhabditis-elegans-chx", "w")
	archivoGuardar.write(secuencia)
	archivoGuardar.close()
#		if j < 7:
#			print(j)
#			print(lineas[i])
#			if j == 1 and ">" not in lineas[i]:
#				print(lineas[i + 1])
#			if j == 2:
#				print(lineas[i + 1])
#			if j == 3: 
#				print(lineas[i + 1])
#			if j == 4:
#				print(lineas[i + 1])
#			if j == 5:
#				print(lineas[i + 1])
#			if j == 6:
#				print(lineas[i + 1])
#			j+=1
#				
#		else:
#			pass;


