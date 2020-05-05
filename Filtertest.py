#! /usr/bin/env python

import sys
import os.path
import aubio
import numpy as np
import matplotlib.pyplot as plt
from mido import MidiFile
from PIL import Image


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
    orig_stdout = sys.stdout
    f = open('bpm.txt', 'w')
    sys.stdout = f
    # in aubio.tempo
    win_s=8192
    hop_s=256
    original = aubio.source(inputfile, hop_size=hop_s)
    samplerate= original.samplerate
    beats =[]
    beatdetection = aubio.tempo("specdiff", win_s, hop_s, samplerate)

    total_Frames=0
    while True:
        samples, read = original()
        beatdetection(samples)                      # Calculate the filter and write it back to the file
        if beatdetection:
            bpm = beatdetection.get_bpm()
            beats.append(bpm)
            #print(temp.get_last_s())               # Write Timestamp of the beat onto console
            print(bpm)                              # Write bpm on console
            total_Frames += read
        if read < original.hop_size:
            break

    sys.stdout = orig_stdout
    calculatebpm = 0
    for i in range(0, beats.__len__()):
        calculatebpm += beats[i]
    calculatebpm = calculatebpm/(beats.__len__()*5) # BPM in in 5 unit interval
    calculatebpm = np.round(calculatebpm)           # round the value to an integer
    calculatebpm = calculatebpm*5                   # get back the old but rounded value
    print(calculatebpm)
    print(total_Frames)


def flip_image(image_path, musicpath):
    """
    Flip or mirror the image
    @param image_path: The path to the image to edit
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(musicpath +'\\' + image_path)
    rotated_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
    rotated_image.save(musicpath +'\\' + image_path)
    #rotated_image.show()
if __name__ == '__main__':
    musicpath = os.getcwd() + "\\Images"
    picturelist = os.listdir(musicpath)
    itterator = 0
    while itterator < len(picturelist):
        if picturelist[itterator].find('left') > 0:
            flip_image(picturelist[itterator], musicpath)
        itterator += 1