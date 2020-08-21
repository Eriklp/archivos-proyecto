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
        self.ventana.setBackground('w')
        self.ventana.setTitle(nombreSolucion, color="b", size="10pt")

        styles = {'color':'b', 'font-size': '10pt'}
        self.ventana.setLabel("left", ejeY, **styles)
        self.ventana.setLabel("bottom", ejeX, **styles)

        self.ventana.addLegend()
        if len(serieY)==2:
            self.plot(serieX, serieY[0], "delta(Dq)", "r")
            # self.plot(serieX, serieY[1], "delta(hq)", "b")

        else:
            if ejeY == "hq" or ejeY == "Dq":
                self.plot(serieX[:-1], serieY[:-1], ejeY, "r")
            else:
                self.plot(serieX, serieY, ejeY, "r")



    def plot(self, x, y, plotname, color):
        pen = pg.mkPen(color=color)
        self.ventana.plot(x, y, name=plotname, pen=pen)
