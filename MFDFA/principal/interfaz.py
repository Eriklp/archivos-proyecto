import gc
import sys
sys.path.append("..")
from interfaz_ui import *
from lecturaArchivos import lectorArchivos
from entidades.segmento import segmento
from entidades.solucion import Solucion
#from mfdfa.mfdfa import mfdfa

lecturas = []
soluciones = []
def openFile(fileName):
    if '.fasta' in fileName or '.fa' in fileName or '.fna' in fileName:

        lectura = lectorArchivos.lectorArchivos(fileName)
        lectura.getName()
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
        self.pushButton.clicked.connect(self.abrirArchivo)
        self.plainTextEdit.setReadOnly(True)
        self.pushButton_4.clicked.connect(self.realizarAnalizisMF)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setText("1")
        self.horizontalSlider.valueChanged.connect(self.actualizarLineEdit)
        self.pushButton_5.clicked.connect(self.borrarSecuencias)

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
        solucionLectura = None
        for lectura in lecturas:
             #dfa = mfdfa(lectura.getSecuenciaNumeros(), rangoQ, tipo)
             #dfa.run()
             lectura.dividirEnArchivos(tamañoSegmentos)
             solucionLectura = lectura.calcularSolucionLectura(tipo, rangoQ)
             solucionLectura.guardarSolucionArchivo()
             soluciones.append(solucionLectura)
        #print(rangoQ, tipo, numeroSegmentos)

    def borrarSecuencias(self):
        self.lecturas = []
        gc.collect()
        print("borrar")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
