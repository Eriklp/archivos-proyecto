import gc
import sys
sys.path.append("..")
from interfaz_ui import *
from lecturaArchivos import lectorArchivos
from entidades.segmento import segmento
from entidades.solucion import Solucion
from entidades.grafica import grafica
#from mfdfa.mfdfa import mfdfa

lecturas = []
soluciones = []
nombresSoluciones = []
def openFile(fileName):
    if '.fasta' in fileName or '.fa' in fileName or '.fna' in fileName:

        lectura = lectorArchivos.lectorArchivos(fileName)
        # lectura.getName()
        lectura.leerArchivoSecuencia()
        lecturas.append(lectura)

    else:
        showdialog("Error", "Debe ser un Archivo Fasta", "Debe ser un archivo Fasta")

def showdialog(title, text, inftext):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)

    msg.setText(text)
    #msg.setInformativeText(inftext)
    msg.setWindowTitle(title)
    #msg.setDetailedText("The details are as follows:")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    #msg.buttonClicked.connect(msgbtn)

    retval = msg.exec_()
    print("value of pressed message box button:", retval)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("software para MFDFA by Erik")
        self.pushButton.clicked.connect(self.abrirArchivo)
        self.plainTextEdit.setReadOnly(True)
        self.pushButton_4.clicked.connect(self.realizarAnalizisMF)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setText("1")
        self.horizontalSlider.valueChanged.connect(self.actualizarLineEdit)
        self.pushButton_5.clicked.connect(self.borrarSecuencias)
        self.pushButton_3.clicked.connect(self.graficarSoluciones)
        self.ventanas = list()
        self.comboBox_4.currentTextChanged.connect(self.mostrarTablaSolucion)

    def abrirArchivo(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filesName, _ = QtWidgets.QFileDialog.getOpenFileNames(None,"seleccionar Archivo", "","All Files (*);;Python Files (*.py)", options=options)
        if filesName:
            for file in filesName:
                openFile(file)

        textoMostrar = "se han cargado: \n \n"
        for nombre in lecturas:
            #print(nombre.getName())
            textoMostrar+= nombre.getName() + "\n"

        self.plainTextEdit.insertPlainText(textoMostrar)

    def actualizarTextEditMF(self, texto):
        self.plainTextEdit_2.appendPlainText(texto+"\n")

    def actualizarLineEdit(self):
        size = str(self.horizontalSlider.value())
        #print(size)
        self.lineEdit.setText(str(size))

    def realizarAnalizisMF(self):
        tipo = int(self.lineEdit.text())
        rangoQ = []
        rangoQs = str(self.comboBox_2.currentText())
        if rangoQs == "-1 a 1":
            rangoQ = [-1, 1]
        elif rangoQs == "-3 a 3":
            rangoQ = [-3, 3]
        elif rangoQs == "-5 a 5":
            rangoQ = [-5, 5]
        elif rangoQs == "-10 a 10":
            rangoQ = [-10, 10]
        elif rangoQs =="-20 a 20":
            rangoQ = [-20, 20]

        tamañoSegmentos = self.spinBox.value()
        # solucionLectura = None
        self.plainTextEdit_2.insertPlainText("Realizando Analizis sobre la secuencias con los siguientes parametros: \n"+
        "tipo: "+str(tipo)+"Rango de exponente Q: "+str(rangoQ)+" Tamaño de segmentos: "+str(tamañoSegmentos)+"\n")
        for lectura in lecturas:
            lectura.dividirEnArchivos(tamañoSegmentos)
            solucionLectura = lectura.calcularSolucionLectura(tipo, rangoQ)
            solucionLectura.guardarSolucionArchivo()
            solucionLectura.guardarSolucionCsv()
            self.actualizarTextEditMF("solucion calculada para: "+solucionLectura.__dict__["nombreSecuencia"])
            soluciones.append(solucionLectura)
            nombresSoluciones.append(solucionLectura.__dict__["nombreSecuencia"])

        self.actualizarTextEditMF("Analilis Multifractal finalizado")
        self.comboBox_4.addItems(nombresSoluciones)

    def graficarSoluciones(self):
        solucionMostrar = self.comboBox_4.currentText()
        ejeX = self.comboBox.currentText()
        ejeY = self.comboBox_3.currentText()
        # print("entro a graficar", ejeX, ejeY, solucionMostrar)
        if ejeX == ejeY:
            showdialog('Error', 'No puede ser el mismo eje', 'no puede ser el mismo eje')
        else:
            for solucion in soluciones:
                if solucionMostrar == solucion.__dict__["nombreSecuencia"]:
                    if ejeX == "q":
                        if ejeY == "hq":
                            conteo = 1
                            for lista in solucion.__dict__["listahqs"]:
                                gra = grafica(solucionMostrar+" parte: "+str(conteo), ejeX, ejeY, solucion.__dict__["listaQ"], lista)
                                self.ventanas.append(gra)
                                gra.show()
                                conteo+=1
                        if ejeY == "Hq":
                            conteo = 1
                            for lista in solucion.__dict__["listaHqs"]:
                                gra = grafica(solucionMostrar+" parte "+str(conteo), ejeX, ejeY, solucion.__dict__["listaQ"], lista)
                                self.ventanas.append(gra)
                                gra.show()
                                conteo+=1
                        if ejeY == "Hq":
                            conteo = 1
                            for lista in solucion.__dict__["listaHqs"]:
                                gra = grafica(solucionMostrar+" parte "+str(conteo), ejeX, ejeY, solucion.__dict__["listaQ"], lista)
                                self.ventanas.append(gra)
                                gra.show()
                                conteo+=1
                        if ejeY == "tq":
                            conteo = 1
                            for lista in solucion.__dict__["listatqs"]:
                                gra = grafica(solucionMostrar+" parte "+str(conteo), ejeX, ejeY, solucion.__dict__["listaQ"], lista)
                                self.ventanas.append(gra)
                                gra.show()
                                conteo+=1
                        if ejeY == "Dq":
                            conteo = 1
                            for lista in solucion.__dict__["listadqm"]:
                                gra = grafica(solucionMostrar+" parte "+str(conteo), ejeX, ejeY, solucion.__dict__["listaQ"], lista)
                                self.ventanas.append(gra)
                                gra.show()
                                conteo+=1

    def mostrarTablaSolucion(self):
        nombreSolucion = self.comboBox_4.currentText()
        for solucion in soluciones:
            if nombreSolucion == solucion.__dict__["nombreSecuencia"]:
                # self.tableWidget = QtWidgets.QTableWidget(len(solucion.__dict__["listaDqs"]), 3, parent = None)
                self.tableWidget.setRowCount(len(solucion.__dict__["listaDqs"]))
                self.tableWidget.setColumnCount(3)
                self.tableWidget.setHorizontalHeaderLabels(["Delta(Dq)", "Delta(hq)", "Cantidad(Alus)"])
                self.tableWidget.verticalHeader().setVisible(True)
                for i in range(len(solucion.__dict__["listaDqs"])):
                    for j in range(3):
                        print(i, j, solucion.__dict__["listaDqs"][i])
                        if j == 0:
                            self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(solucion.__dict__["listaDqs"][i])))
                        if j == 1:
                            self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(solucion.__dict__["listadqs"][i])))
                        if j == 2:
                            self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(solucion.__dict__["listaAlus"][i])))
                self.tableWidget.resizeColumnsToContents()
                gra = grafica(nombreSolucion, "segmento", "delta(Dq) - delta(hq)", range(len(solucion.__dict__["listaDqs"])), [solucion.__dict__["listaDqs"], solucion.__dict__["listadqs"]])
                self.ventanas.append(gra)
                gra.show()


    def borrarSecuencias(self):
        lecturas = []
        gc.collect()
        print("borrar")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
