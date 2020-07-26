

class segmento(object):
    """docstring for segmento."""

    nombreSecuencia = ""
    contenidoSegmento = []

    def __init__(self, nombreSecuencia, contenidoSegmento):
        super(segmento, self).__init__()
        self.nombreSecuencia = nombreSecuencia
        self.contenidoSegmento = contenidoSegmento

    def getNombreSecuencia(self):
        return str(self.nombreSecuencia)

    def getindInicial(self):
        return self.indInicial

    def getIndFinal(self):
        return self.indFinal

    def getContenidoSegmento(self):
        return self.contenidoSegmento

    def leerArchivoSegmento():
        pass
