import sys
import pandas as pd
sys.path.append("..")

class Solucion(object):
    """docstring for Solucion."""
    nombreSecuencia = ""
    ventanas = []
    listaQ = []
    listaHqs = []
    listatqs = []
    listahqs = []
    listaFlucts =[]
    listaDqs =[]
    listadqs = []
    listadqm  = []
    listaAlus = []



    def __init__(self, nombre, ventanas, listaQ, listaHqs, listatqs, listahqs, listaFlucts, listaDqs, listadqs, listadqm, listaAlus):
        super(Solucion, self).__init__()
        self.nombreSecuencia = nombre
        self.ventanas = ventanas
        self.listaQ = listaQ
        self.listaHqs = listaHqs
        self.listatqs = listatqs
        self.listahqs = listahqs
        self.listaFlucts = listaFlucts
        self.listaDqs =  listaDqs
        self.listadqs = listadqs
        self.listadqm = listadqm
        self.listaAlus = listaAlus

    def guardarSolucionArchivo(self):
        # print(self.__dict__)
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
        info+="listatqs: "
        for i in self.__dict__['listatqs']:
            info+="{}".format(i)+ ", "
        info +="\n"
        info+="listahqs: "
        for i in self.__dict__['listahqs']:
            info+="{}".format(i)+ ", "
        info +="\n"
        info+="listadqm: "
        for i in self.__dict__['listadqm']:
            info+="{}".format(i)+ ", "
        info +="\n"
        # info+="listaFlucts: "
        # for i in self.__dict__['listaFlucts']:
        #     info+="{}".format(i)+ ", "
        # info +="\n"
        info+="listaDqs: "
        for i in self.__dict__['listaDqs']:
            info+="{}".format(i)+ ", "
        info +="\n"
        info+="listadqs: "
        for i in self.__dict__['listadqs']:
            info+="{}".format(i)+ ", "
        info +="\n"
        info+="listaAlus: "
        for i in self.__dict__['listaAlus']:
            info+="{}".format(i)+ ", "
        with open("../files/soluciones/"+self.nombreSecuencia, 'w') as f:
            f.write(info)

    def guardarSolucionCsv(self):
        # info = self.__dict__
        listaHq = []
        listatq = []
        listahqs = []
        listadqms = []
        for i in self.__dict__['listaHqs']:
            for j in i:
                listaHq.append(j)

        for i in self.__dict__['listatqs']:
            for j in i:
                listatq.append(j)

        for i in self.__dict__['listahqs']:
            for j in i:
                listahqs.append(j)

        for i in self.__dict__['listadqm']:
            for j in i:
                listadqms.append(j)

        print(len(listaHq), len(listatq), len(listahqs))
        info = {
            'Hqs': listaHq,
            'tqs': listatq,
            'hqs': listahqs,
            'dqm': listadqms
        }
        pd.DataFrame(info).T.reset_index().to_csv('../files/soluciones/'+self.nombreSecuencia+'.csv', header = False, index = False)