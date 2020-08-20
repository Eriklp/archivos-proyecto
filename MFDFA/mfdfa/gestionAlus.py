import subprocess
import sys
sys.path.append("..")
def contarAlus(rutaArchivo):
    subprocess.call(['RepeatMasker', '-alu', rutaArchivo], stdout=subprocess.PIPE,)
    subprocess.call(['/usr/local/RepeatMasker/./RepeatMasker', '-alu', rutaArchivo], stdout=subprocess.PIPE,)

def obtenerCantidadAlus(archivo_tbl):
    numeroAlus = subprocess.check_output("awk 'NR==12' "+archivo_tbl+" | awk  '{print $2}'")
    numeroAlus = subprocess.check_output("awk 'NR==12' "+archivo_tbl+" | awk  '{print $2}'", shell = True)
    print(numeroAlus)
    return numeroAlus
