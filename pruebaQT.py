import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

#imports juegos del caos 
import collections
from collections import OrderedDict
from matplotlib import pyplot as plt
from matplotlib import cm
import pylab
import math
from scipy import signal
import numpy as np
#f = open('/home/erik/pylori26695_Eslice.fasta')
#s1 = f.read()
#data = "".join(s1.split("\n")[1:])


#imports para manejo de octave

from oct2py import octave, Oct2Py

#-------------------------------------------------------------------------------------------------------
lendata = 0

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
        plt.figure()
        oc = Oct2Py()
        oc.myDetrend(caracteres)
        # x = np.linspace(0, len(listaNumero), 1000)
        # resultadoDetrend = signal.detrend(x)
        # print(signal.detrend(listaNumero))
        # plt.plot(x, resultadoDetrend, label="detrend")
        # plt.show()
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


    

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.openFileNameDialog()
        #self.openFileNamesDialog()
        #self.saveFileDialog()
        
        self.show()
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            openFile(fileName)
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())