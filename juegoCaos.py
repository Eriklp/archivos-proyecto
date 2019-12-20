import __future__
import collections
from collections import OrderedDict
from matplotlib import pyplot as plt
from matplotlib import cm
import pylab
import math
f = open("/home/erik/pylori26695_Eslice.fasta")
s1 = f.read()
data = "".join(s1.split("\n")[1:])
 
def count_kmers(sequence, k):
    d = collections.defaultdict(int)
    for i in range(len(data)-(k-1)):
        d[sequence[i:i+k]] +=1
    for key in list(d.keys()):
        if "N" in key:
            del d[key]
    return d
 
def probabilities(kmer_count, k):
    probabilities = collections.defaultdict(float)
    N = len(data)
    for key, value in list(kmer_count.items()):
        probabilities[key] = float(value) / (N - k + 1)
    return probabilities
 
def chaos_game_representation(probabilities, k):
    array_size = int(math.sqrt(4**k))
    chaos = []
    for i in range(array_size):
        chaos.append([0]*array_size)
 
    maxx = array_size
    maxy = array_size
    posx = 1
    posy = 1
    for key, value in list(probabilities.items()):
        for char in key:
            if char == "T":
                posx += maxx / 2
            elif char == "C":
                posy += maxy / 2
            elif char == "G":
                posx += maxx / 2
                posy += maxy / 2
            maxx = maxx / 2
            maxy /= 2
        chaos[posy-1][posx-1] = value
        maxx = array_size
        maxy = array_size
        posx = 1
        posy = 1
 
    return chaos
 
f3 = count_kmers(data, 3)
f4 = count_kmers(data, 4)
 
f3_prob = probabilities(f3, 3)
f4_prob = probabilities(f4, 4)
 
chaos_k3 = chaos_game_representation(f3_prob, 3)
pylab.title('Chaos game representation for 3-mers')
pylab.imshow(chaos_k3, interpolation='nearest', cmap=cm.gray_r)
pylab.show()
 
chaos_k4 = chaos_game_representation(f4_prob, 4)
pylab.title('Chaos game representation for 4-mers')
pylab.imshow(chaos_k4, interpolation='nearest', cmap=cm.gray_r)
pylab.show()