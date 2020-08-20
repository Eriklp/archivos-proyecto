from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

class grafica(QtWidgets.QMainWindow):
    nombreSolucion = ""
    ejeX = ""
    ejeY = ""
    serieX = []
    serieY = []
    def __init__(self, nombreSolucion, ejeX, ejeY, serieX, serieY):
        QtWidgets.QMainWindow.__init__(self)
        self.nombreSolucion = nombreSolucion
        self.ejeX = ejeX
        self.ejeY = ejeY
        self.serieX = serieX
        self.serieY = serieY

        self.ventana = pg.PlotWidget()
        self.setCentralWidget(self.ventana)
        self.ventana.setTitle(nombreSolucion, color="b", size="10pt")
        # styles = {'color':'b', 'font-size': '10pt'}
        self.ventana.setLabel("left", ejeY, color="b", size="10pt")
        self.ventana.setLabel("bottom", ejeX, color="b", size="10pt")
        if ejeY == "hq" or ejeY == "Dq":
            self.ventana.plot(serieX[:-1], serieY[:-1])
        else:
            self.ventana.plot(serieX, serieY)
