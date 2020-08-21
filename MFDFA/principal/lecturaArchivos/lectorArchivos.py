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
import threading
import time

def divisionArreglo(arr, tamaño):
    arrs = []
    while len(arr) > tamaño:
        pice = arr[:tamaño]
        arrs.append(pice)
        arr   = arr[tamaño:]
    arrs.append(arr)
    return arrs

def diff(arreglo):
    derivada = [len(arreglo)]
    derivada[0] = 1
    for i in range(1, len(arreglo)):
        derivada.append(arreglo[i] - arreglo[i - 1])
    print(derivada)
    return np.array(derivada)

def obtenerConteos(nombreSecuencia):
        listaConteo = []
        listaArchivos = [archivo for archivo in scandir("../files") if archivo.name.endswith(".fa.tbl") and nombreSecuencia in archivo.name]
        for archivo in listaArchivos:
            print(archivo.name)
            numero = int(archivo.name[-9:-7])
            cantidadalus = int(subprocess.check_output("awk 'NR==12' ../files/"+archivo.name+" | awk '{print $2}'" , shell = True))
            elemento = (numero, cantidadalus)
            print(elemento)
            listaConteo.append(elemento)
        listaConteo = sorted(listaConteo)
        print(listaConteo)
        return listaConteo
def realizarConteos(nombreSecuencia):
    print("entro a conteo", nombreSecuencia)
    # contarAlus("../files/"+nombreSecuencia+"*.fa")
    p = subprocess.run("/usr/local/RepeatMasker/./RepeatMasker -alu ../files/"+nombreSecuencia+"*.fa", shell=True, stdout=subprocess.PIPE)
    print("returnCode:", p.returncode)


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
            self.segmentos.append(self.secuenciaNumeros)
        else:
            print("tamaño: ", tamañoSegmentos)
            subprocess.call(['split', '-b', str(tamañoSegmentos)+"MB", '--numeric-suffixes', self.archivo, '../files/'+self.nombre])
            with scandir("../files/") as archivos:
                for archivo in archivos:
                    if self.nombre in archivo.name and archivo.is_file():
                        nuevoNombre = ("../files/"+archivo.name+".fa").replace(" ", "_").replace(">", "_").replace("|", "").replace("(", "").replace(")", "")
                        print(nuevoNombre)
                        # rename("../files/"+archivo.name, (("../files/"+archivo.name+".fa").replace(" ", "_").replace(">", "_").replace("|", "").replace("(", "").replace(")", "")))
                        rename("../files/"+archivo.name, nuevoNombre)
                        # contarAlus(nuevoNombre)
                # for archivos in archivos:
                #     if archivo.name.endswith(".fa"):
                #         ccontarAlus("..files/"+archivo.name)

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
        hiloConteos = threading.Thread(target=realizarConteos, args=(nombre, ))
        hiloConteos.start()
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
        listaAlusSegmentos =[]
        #Se realiza el mfdfa en cada segmento
        solucion = None
        for segmento in self.segmentos:
            Hq = []
            fluct = []
            tq = []
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
            hq = np.append(hq, 0.6)
            print("listahq: ")
            print(hq.tolist())
            listaHqSegmentos.append(Hq)
            listatqSegmentos.append(tq)
            listahqSegmentos.append(hq.tolist())
            dqm = (q*hq) - np.array(tq)
            listadqmSegmentos.append(dqm.tolist())

            deltaDq = max(dqm.tolist()) - min(dqm.tolist())
            deltahq = hq[0] - hq[-2]
            # print("Hq-1:{}-Hq0:{}".format(Hq[-1], Hq[0]))
            listaDqSegmentos.append(deltaDq)
            listadqSegmentos.append(deltahq)

            print("listaDqs: ", listaDqSegmentos)
            listaFLuctsSegmentos.append(fluct)

        while hiloConteos.isAlive():
            print("aun no termina de contar Alus")
            time.sleep(30)
        listaConteosTuplas = obtenerConteos(nombre)
        for i in range(len(listaDqSegmentos)):
            listaAlusSegmentos.append(listaConteosTuplas[i][1])

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
