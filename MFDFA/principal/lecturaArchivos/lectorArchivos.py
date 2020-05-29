

class lectorArchivos:
    nombre = ""
    archivo = ""
    secuencia = ""
    secuenciaNumeros = []

    def __init__(self, archivo):
        self.archivo = archivo

    def leerArchivoSecuencia(self):
        print(self.archivo)
        try:
            f = open(self.archivo)
            s1 = f.read()
            print(s1.split("\n")[:1])
            data = "".join(s1.split("\n")[1:]).upper()
            print(len(data))
            listaNumero = []
            #caracteres = []
            for char in data:
                if char == "A":
                    listaNumero.append(0)
                    #caracteres.append("A")
                if char == "T":
                    listaNumero.append(1)
                    #caracteres.append("G")
                if char == "G":
                    listaNumero.append(2)
                    #caracteres.append("G")
                if char == "C":
                    listaNumero.append(3)
                    #caracteres.append("C")
            print(data[0:7])
            #print(caracteres[0:7])
            print(listaNumero[0:7])
            self.secuencia = data
            self.secuenciaNumeros = listaNumero

        except Exception as error:
            print(str(error))


    def getName(self):
        print(self.nombre)
        return self.nombre

    def getSecuencia(self):
        #print(self.secuencia)
        return self.secuencia

    def getSecuenciaNumeros(self):
        return self.secuenciaNumeros
