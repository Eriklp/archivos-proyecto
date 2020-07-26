import subprocess
import sys
sys.path.append("..")
def contarAlus(rutaArchivo):
        subprocess.Popen(['/usr/local/RepeatMasker/./RepeatMasker', '-alu', '-dir', '/root/archivos-proyecto/MFDFA/files/resultsalus', rutaArchivo], stdout=subprocess.PIPE,)
