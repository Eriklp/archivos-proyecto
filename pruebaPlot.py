from oct2py import octave

import numpy as np
import os

import pprint

print(octave.plus(2, 3))
octave.run('pruebaPlot.m')
print(octave.who())
