import subprocess
import sys
sys.path.append("..")
def contarAlus(rutaArchivo):
    subprocess.Popen(['/usr/local/RepeatMasker/./RepeatMasker', '-alu', '../files', rutaArchivo], stdout=subprocess.PIPE,)

def obtenerCantidadAlus(archivo_tbl):
    numeroAlus = subprocess.check_output("awk 'NR==12' "+archivo_tbl+" | awk  '{print $2}'")
    print(numeroAlus)
    return numeroAlus
