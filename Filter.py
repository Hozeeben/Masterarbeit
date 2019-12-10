#! /usr/bin/env python

import sys, os.path
import aubio
from numpy import zeros, log10, vstack
import matplotlib.pyplot as plt

filename = 'KIRA New World.wav'
downsample = 1
samplerate = 44100 // downsample
win_s = 512 // downsample # fft size
hop_s = 256 // downsample # hop size

original = aubio.source(filename, samplerate, hop_s)
snk=aubio.sink('Copied.wav')
while True:
    samples, read = original()  # read file insert filter code below


    snk.do(aubio.fvec(samples),hop_s)
    if read < original.hop_size: break
snk.close()