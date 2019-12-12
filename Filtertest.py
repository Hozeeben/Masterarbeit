#! /usr/bin/env python

import sys
import os.path
import aubio
import numpy as np


def apply_filter(path, target):
    # open input file, get its samplerate
    s = aubio.source(path)
    samplerate = s.samplerate

    # create an A-weighting filter (Biquad)
    f = aubio.digital_filter(3)
    # f.set_a_weighting(samplerate)
    f.set_biquad(1.31235898*10**-4, 2.62471796*10**-4, 1.31235898*10**-4, -1.98642633, 0.98695127)  # Kombi von 2 FIlter(Lowshelf+Lowpass)

    # create output file
    o = aubio.sink(target, samplerate)

    total_frames = 0
    while True:
        # read from source
        samples, read = s()
        # filter samples
        filtered_samples = f(samples)
        # write to sink
        o(filtered_samples, read)
        # count frames read
        total_frames += read
        # end of file reached
        if read < s.hop_size:
            break

def bpmdetection(inputfile):
    print('Hello Function')
    # in aubio.tempo
    win_s=8192
    hop_s=256
    original = aubio.source(inputfile, hop_size=hop_s)
    #aubio.source()
    samplerate= original.samplerate
    beats =[]
    temp = aubio.tempo("specdiff", win_s, hop_s, samplerate)
    while True:
        samples, read = original()
        beat = temp(samples)                      # Calculate the filter and write it back to the file
        if temp:
            bpm =temp.get_bpm()
            beats.append(bpm)
        #print(bpm)
        if read < original.hop_size:
            break

    calculatebpm=0
    print(np.min(beats))
    print(np.median(beats))
    print(np.max(beats))
    #for i in range(0, beats.__len__()):
    #    beats.sort()
    #    print(beats[i])                            #ToDO: Überlegen wie BPM richtig berechnet werden können (mehr Tests machen mit anderen Tracks)

if __name__ == '__main__':
    outputlow = 'Test'
    #writelowpass = aubio.sink(outputlow, samplerate)
    input_path='NIVIRO - Flashes.wav'
    input_path2 = 'KIRA New World.wav'
    #output_path= 'KIRA New World Filtered.wav'
    #apply_filter(input_path, output_path)
    bpmdetection(input_path)
    bpmdetection(input_path2)