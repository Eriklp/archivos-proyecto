import sys
sys.path.append("..")

class Solucion(object):
    """docstring for Solucion."""
    nombreSecuencia = ""
    ventanas = []
    listaQ = []
    listaHqs = []
    listaFlucts =[]
    listaDqs =[]
    listaAlus = []



    def __init__(self, nombre, ventanas, listaQ, listaHqs, listaFlucts, listaDqs, listaAlus):
        super(Solucion, self).__init__()
        self.nombreSecuencia = nombre
        self.ventanas = ventanas
        self.listaQ = listaHqs
        self.listaFlucts = listaFlucts
        self.listaDqs =  listaDqs
        self.listaAlus = listaAlus

    def guardarSolucionArchivo(self):
        info = "nombre: "+self.__dict__['nombreSecuencia']+"\n"
        info += "ventanas: "
        for i in self.__dict__['ventanas']:
            info+="{}".format(i)+", "
        info +="\n"
        info+="listaQ: "
        for i in self.__dict__['listaQ']:
            info+="{}".format(i)+ ", "
        info +="\n"
        info+="listaHqs: "
        for i in self.__dict__['listaHqs']:
            info+="{}".format(i)+ ", "
        info +="\n"
        info+="listaFlucts: "
        for i in self.__dict__['listaFlucts']:
            info+="{}".format(i)+ ", "
        info +="\n"
        info+="listaDqs: "
        for i in self.__dict__['listaDqs']:
            info+="{}".format(i)+ ", "
        info +="\n"
        with open("../files/soluciones/"+self.nombreSecuencia, 'w') as f:
            f.write(info)
