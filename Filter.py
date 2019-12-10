#! /usr/bin/env python

import sys, os.path
import aubio
from numpy import zeros, log10, vstack
import matplotlib.pyplot as plt
orig_stdout=sys.stdout
f=open('outputcvecbefore.txt', 'w')
sys.stdout=f

filename = 'KIRA New World.wav'
downsample = 1
samplerate = 44100 // downsample
win_s = 512 // downsample # fft size
hop_s = 256 // downsample # hop size

original = aubio.source(filename, samplerate, hop_s)
snk=aubio.sink('Copied.wav')
while True:
    samples, read = original()  # read file insert filter code below
    #Test
    x = aubio.fvec(samples)
    pv = aubio.pvoc(512, 256)                           #Wird irgendwas bei pvoc gerechnet?
    y = aubio.cvec(512)
    myfvec=pv(x)                                         #Type:cvec 257
    #mycvec=y(pv(x))
    reconstructed=pv.rdo(myfvec)
    #print(reconstructed)
    
    snk.do(aubio.fvec(reconstructed),hop_s)
    if read < original.hop_size: break
snk.close()
#Löschen
sys.stdout=orig_stdout
f.close()
