import numpy as np
import sys
from os import rename, scandir, path
import subprocess
sys.path.append("..")
import matplotlib.pyplot as plt
from mfdfa.mfdfa import MFDFA
from entidades.segmento import segmento
from mfdfa.gestionAlus import contarAlus
from entidades.solucion import Solucion

def divisionArreglo(arr, tamaño):
    arrs = []
    while len(arr) > tamaño:
        pice = arr[:tamaño]
        arrs.append(pice)
        arr   = arr[tamaño:]
    arrs.append(arr)
    return arrs

class lectorArchivos:
    nombre = ""
    archivo = ""
    #secuencia = ""
    secuenciaNumeros = []
    segmentos = []
    def __init__(self, archivo):
        self.archivo = archivo

    def leerArchivoSecuencia(self):
        print(self.archivo)
        try:
            f = open(self.archivo)
            s1 = f.read()
            #print(s1.split("\n")[:1])
            self.nombre = str(s1.split("\n")[:1][0])+' '
            data = "".join(s1.split("\n")[1:]).upper()
            #print(len(data))
            listaNumero = []
            #caracteres = []
            for char in data:
                if char == "A":
                    listaNumero.append(np.float64(1))
                    #caracteres.append("A")
                if char == "T":
                    listaNumero.append(np.float64(2))
                    #caracteres.append("G")
                if char == "G":
                    listaNumero.append(np.float64(3))
                    #caracteres.append("G")
                if char == "C":
                    listaNumero.append(np.float64(4))
                    #caracteres.append("C")
                # if char =="N":
                #      listaNumero.append(0)
            print(data[0:7])
            #print(caracteres[0:7])
            print(listaNumero[0:7])
            #self.secuencia = data
            self.secuenciaNumeros = listaNumero

        except Exception as error:
            print(str(error))

    def dividirEnArchivos(self, tamañoSegmentos):
        if tamañoSegmentos == 0:
            pass
        else:
            subprocess.call(['split', '--bytes', str(tamañoSegmentos)+"M", '--numeric-suffixes', self.archivo, '../files/'+self.nombre])
            with scandir("../files/") as archivos:
                for archivo in archivos:
                    if self.nombre in archivo.name:
                        rename("../files/"+archivo.name, ("../files/"+archivo.name+".fa").replace(" ", "_"))
                        #print(archivo.name)

        ##Se crean los objeto segmento los cuales contendran secuencias del tamaño indicado para cada lectura
            arregloTemporal = divisionArreglo(self.secuenciaNumeros, (tamañoSegmentos*1000000))
            del self.secuenciaNumeros
            for arreglo in arregloTemporal:
                segmentoT = segmento(self.nombre, arreglo)
                self.segmentos.append(segmentoT)
                del segmentoT


        #print(self.segmentos[0].__dict__['contenidoSegmento'])

    def calcularSolucionLectura(self, tipo, q):
        #lag = np.linspace(1000, 64000, num = 10).astype(int)
        nombre = self.nombre
        lag = np.array([1000, 5000, 10000, 20000, 30000, 50000, 80000, 100000, 120000, 150000, 200000])
        q = np.linspace(q[0], q[1], num = 10)
        listaHqSegmentos = []
        listaFLuctsSegmentos =[]
        listaDqSegmentos =[]
        listaAlusSegmentos =[]
        #Se realiza el mfdfa en cada segmento
        solucion = None
        for segmento in self.segmentos:
            hq = []
            fluct = []
            for e in q:
                l, f = MFDFA(np.array(segmento.__dict__["contenidoSegmento"]),
                lag,
                tipo,
                e)
                coeff = np.polyfit(np.log(l), np.log(f), tipo)[0]
                print(coeff)
                hq.append(coeff)
                fluct.append(f)
            listaHqSegmentos.append(hq)
            listaDqSegmentos.append(max(hq) - min(hq))
            listaFLuctsSegmentos.append(fluct)
            #se realiza el conteo de alus para cada segmento pasando el nombre de su secuencia
            with scandir("../files") as archivos:
                for archivo in archivos:
                    if self.nombre in archivo.name and archivo.name.endswith('.fa'):
                        rutaArchivoSegmento = path.abspath(archivo.name)
                        contarAlus(rutaArchivoSegmento)
                #for para obtener la cantidad de alus luego de contarlas para cada segmento
                for i in range(len(self.segmentos)):
                    if self.nombre in archivo.name and archivo.name.endswith(i+'.fa.tbl'):
                        rutaArchivoTblSegmento = path.abspath(archivo.name)
                        listaAlusSegmentos.append(obtenerCantidadAlus(rutaArchivoTblSegmento))

        solucion = Solucion(nombre, lag, q, listaHqSegmentos, listaFLuctsSegmentos, listaDqSegmentos, listaAlusSegmentos)

        return solucion



        # q = np.linspace(q[0], q[1], num = 10)
        # #lag = np.linspace(1000, 64000, num = 10).astype(int)
        # lag = np.array([1000, 5000, 10000, 20000, 30000, 50000, 80000, 100000, 120000, 150000, 200000])
        # hq = []
        # for e in q:
        #     l, f = MFDFA(np.array(self.secuenciaNumeros),
        #     lag,
        #     tipo,
        #     e)
        #     coeff = np.polyfit(np.log(l), np.log(f), tipo)[0]
        #     print(coeff)
        #     hq.append(coeff)
        #
        # plt.plot(q, hq, 'o', label="bla")
        #
        # plt.show()


    def getName(self):
        #print(self.nombre)
        return self.nombre

    def getSecuencia(self):
        #print(self.secuencia)
        return self.secuencia

    def getSecuenciaNumeros(self):
        return self.secuenciaNumeros
