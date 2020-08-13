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

class lectorArchivos(object):
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
            self.nombre = str(s1.split("\n")[:1][0]).replace(' ', '_').replace(">", "").replace(";", "")
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
            if 'N' in data:
                self.archivo = self.archivo.replace(".fa", " sinNs.fa")
                f2 = open(self.archivo, 'w')
                print("remplazo de N")
                data = data.replace('N', '')
                info = self.nombre+'\n'
                contador = 0
                for char in data:
                    if contador <70:
                        info+=char 
                        contador +=1
                    else:
                        info+='\n'
                        info+=char
                        contador = 1

                f2.write(info)
                f2.close()
            f.close()
        except Exception as error:
            print(str(error))

    def dividirEnArchivos(self, tamañoSegmentos):
        self.segmentos = []
        if tamañoSegmentos == 0:
            pass
        else:
            print("tamaño: ", tamañoSegmentos)
            subprocess.call(['split', '--bytes', str(tamañoSegmentos)+"M", '--numeric-suffixes', self.archivo, '../files/'+self.nombre])
            with scandir("../files/") as archivos:
                for archivo in archivos:
                    if self.nombre in archivo.name and archivo.is_file():
                        rename("../files/"+archivo.name, (("../files/"+archivo.name+".fa").replace(" ", "_")).replace(">", "_").replace("|", "").replace("(", "").replace(")", ""))
                        #print(archivo.name)

        ##Se crean los objeto segmento los cuales contendran secuencias del tamaño indicado para cada lectura
            arregloTemporal = divisionArreglo(self.secuenciaNumeros, (tamañoSegmentos*1000000))
            self.secuenciaNumeros = []
            for arreglo in arregloTemporal:
                print(len(arreglo))
                segmentoT = segmento(self.nombre, arreglo)
                self.segmentos.append(segmentoT)

        
        print("tamaño segmentos dividir: ",len(self.segmentos))

    def calcularSolucionLectura(self, tipo, q):
        #lag = np.linspace(1000, 64000, num = 10).astype(int)
        nombre = self.nombre
        lag = np.array([1000, 5000, 10000, 20000, 30000, 50000, 80000, 100000, 120000, 150000, 200000, 220000, 250000])
        q = np.linspace(q[0], q[1], num = 10)
        deltaQ = q[1] - q[0]
        listaHqSegmentos = []
        listatqSegmentos = []
        listahqSegmentos = []
        listaFLuctsSegmentos =[]
        listaDqSegmentos =[]
        listadqSegmentos = []
        listadqmSegmentos = []
        #Se realiza el mfdfa en cada segmento
        solucion = None
        for segmento in self.segmentos:
            Hq = []
            fluct = []
            tq = []
            listaAlusSegmentos =[]
            for e in q:
                print("longitud de segmentos:", len(self.segmentos))
                l, f = MFDFA(np.array(segmento.__dict__["contenidoSegmento"]),
                lag,
                tipo,
                e)
                Hqv = np.polyfit(np.log(l), np.log(f), tipo)[0]
                print(Hqv)
                Hq.append(Hqv[0])
                tq.append((Hqv[0]*e) - 1)
                fluct.append(f)
            print("listHq:")
            print(Hq)
            print("listatq: ")
            print(tq)
            hq = (np.diff(tq)/deltaQ)
            # hq = np.concatenate((hq, diff))
            # TODO: implementar una aproximacion para el ultimo valor de hq ya que
            # se pierde durante la derivacion de tq
            hq = np.append(hq, 0.5)
            print("listahq: ")
            print(hq.tolist())
            listaHqSegmentos.append(Hq)
            listatqSegmentos.append(tq)
            listahqSegmentos.append(hq.tolist())
            # for i in q:

            Dq = Hq[0] - Hq[-1]
            dq = hq[0] - hq[-2]
            # print("Hq-1:{}-Hq0:{}".format(Hq[-1], Hq[0]))
            listaDqSegmentos.append(Dq)
            listadqSegmentos.append(dq)
            dqm = (q*hq) - np.array(tq)
            listadqmSegmentos.append(dqm.tolist())
            print("listaDqs: ", listaDqSegmentos)
            listaFLuctsSegmentos.append(fluct)
            #se realiza el conteo de alus para cada segmento pasando el nombre de su secuencia
            # self.segmentos.remove(segmento)
        with scandir("../files/") as archivos:
            print("entro a scandir")
            for archivo in archivos:
                if segmento.__dict__["nombreSecuencia"] in archivo.name and archivo.name.endswith('.fa'):
                    print("conteo alus: {}-{}".format(archivo.name, self.nombre))
                    rutaArchivoSegmento = path.abspath(archivo.name)
                    print(rutaArchivoSegmento)
                    contarAlus(rutaArchivoSegmento)
                
                #for para obtener la cantidad de alus luego de contarlas para cada segmento
                # for i in range(len(self.segmentos)):
                #     if self.nombre in archivo.name and archivo.name.endswith(str(i)+'.fa.tbl'):
                #         print("entro a scandir tbl")
                #         rutaArchivoTblSegmento = path.abspath(archivo.name)
                #         listaAlusSegmentos.append(obtenerCantidadAlus(rutaArchivoTblSegmento))
        
        solucion = Solucion(nombre, lag, q, listaHqSegmentos, listatqSegmentos, listahqSegmentos, listaFLuctsSegmentos, listaDqSegmentos, listadqSegmentos, listadqmSegmentos, listaAlusSegmentos)

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
