from interfaz_ui import *

def openFile(fileName):
    if '.fasta' in fileName:
        f = open(fileName)
        s1 = f.read()
        data = "".join(s1.split("\n")[1:]).upper()
        print(len(data))
        lendata = len(data)
        listaNumero = []
        caracteres = []
        for char in data:
            if char == "A":
                listaNumero.append(0)
                caracteres.append("A")
            if char == "T":
                listaNumero.append(1)
                caracteres.append("G")
            if char == "G":
                listaNumero.append(2)
                caracteres.append("G")
            if char == "C":
                listaNumero.append(3)
                caracteres.append("C")
        print(data[0:7])
        print(listaNumero[0:7])

    else:
        showdialog("Error", "Debe ser un Archivo Fasta", "Debe ser un archivo Fasta")


def showdialog(title, text, inftext):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText(text)
    #msg.setInformativeText(inftext)
    msg.setWindowTitle(title)
    #msg.setDetailedText("The details are as follows:")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    #msg.buttonClicked.connect(msgbtn)

    retval = msg.exec_()
    print("value of pressed message box button:", retval)

def abrirArchivo():
    ventana = MyFileDialog()
    ventana.initUI()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
   def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(abrirArchivo)



class MyFileDialog(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Seleccionar los archivos .FASTA'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #self.openFileNameDialog()
        self.openFileNamesDialog()
        #self.saveFileDialog()

        self.show()

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            openFile(fileName)

    def openFileNamesDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
