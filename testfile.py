#! /usr/bin/env python

import sys
import aubio
#from aubio import source, notes

filename = 'KIRA New World.wav'
orig_stdout=sys.stdout
downsample = 1
samplerate = 44100 // downsample
win_s = 512 // downsample # fft size
hop_s = 256 // downsample # hop size

original = aubio.source(filename, samplerate, hop_s)
f=open('outputfvec.txt', 'w')
sys.stdout=f
#for frames in original:
#    print(frames)

snk=aubio.sink('Copied.wav')
#samplerate = s.samplerate

#tolerance = 0.8
while True:
    samples, read = original()  # read file
    #for i in range (0, hop_s):
    snk.do(aubio.fvec(samples),hop_s)                 #hop_s ist wieviel aus jedem sample geschrieben werden
    #print(aubio.fvec(samples))
    if read < original.hop_size: break
snk.close()
sys.stdout=orig_stdout
f.close()

#notes_o = aubio.notes("default", win_s, hop_s, samplerate)
#print("%8s" % "time","[ start","vel","last ]")
## total number of frames read
#total_frames = 0
#while True:
#    samples, read = s()
#    new_note = notes_o(samples)
#    new_midi = aubio.note2midi(new_note)
#    if (new_note[0] != 0):
#        note_str = ' '.join(["%.2f" % i for i in new_note])
#        print("%.6f" % (total_frames/float(samplerate)), new_note)
#    total_frames += read
#    if read < hop_s: break

