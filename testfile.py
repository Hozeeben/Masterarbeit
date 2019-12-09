#! /usr/bin/env python

import sys
import aubio
#from aubio import source, notes

filename = 'KIRA New World.wav'

downsample = 1
samplerate = 44100 // downsample
win_s = 512 // downsample # fft size
hop_s = 256 // downsample # hop size

s = aubio.source(filename, samplerate, hop_s)
samplerate = s.samplerate

tolerance = 0.8

notes_o = aubio.notes("default", win_s, hop_s, samplerate)

print("%8s" % "time","[ start","vel","last ]")

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    new_note = notes_o(samples)
    new_midi = aubio.note2midi(new_note)
    if (new_note[0] != 0):
        note_str = ' '.join(["%.2f" % i for i in new_note])
        print("%.6f" % (total_frames/float(samplerate)), new_note)
    total_frames += read
    if read < hop_s: break

