from interfaz_ui import *
import lectorArchivos


def openFile(fileName):
    if '.fasta' in fileName or '.fa' in fileName or '.fna' in fileName:
        
        #f = open(fileName)
        #s1 = f.read()
        #data = "".join(s1.split("\n")[1:]).upper()
        #print(len(data))
        #lendata = len(data)
        #listaNumero = []
        #caracteres = []
        #for char in data:
        #    if char == "A":
        #        listaNumero.append(0)
        #        caracteres.append("A")
        #    if char == "T":
        #        listaNumero.append(1)
        #        caracteres.append("G")
        #    if char == "G":
        #        listaNumero.append(2)
        #        caracteres.append("G")
        #    if char == "C":
        #        listaNumero.append(3)
        #        caracteres.append("C")
        #print(data[0:7])
        #print(listaNumero[0:7])

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

def abrirArchivo():
    #ventana = MyFileDialog()
    #ventana.initUI()
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.DontUseNativeDialog
    filesName, _ = QtWidgets.QFileDialog.getOpenFileNames(None,"seleccionar Archivo", "","All Files (*);;Python Files (*.py)", options=options)
    if filesName:
        print(filesName)
        for file in filesName:
            openFile(file)
        ##openFile(filesName)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
   def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(abrirArchivo)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
