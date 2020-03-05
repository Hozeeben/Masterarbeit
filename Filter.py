#! /usr/bin/env python

import sys, os.path
import aubio
import numpy as np
import matplotlib.pyplot as plt
import shutil


def bpmdetection(inputfile):
    orig_stdout = sys.stdout
    f = open('bpm.txt', 'w')
    sys.stdout = f
    win_s = 8192
    hop_s = 256
    original = aubio.source(inputfile, hop_size=hop_s)
    samplerate = original.samplerate
    beats = []
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

def lowpassfilter(inputfile, outputlow):
    original = aubio.source(inputfile)                          # Open the original file
    samplerate = original.samplerate                              # get samplerate for output file
    writetofile = aubio.sink(outputlow, samplerate)            # Create Output sink

    # Biquad Filter as Low-Pass-Filter
    # Center Frequency 150
    # Samplerate 41000
    # Q 0.75
    calculatefilter = aubio.digital_filter(3)
    calculatefilter.set_biquad(1.30104102 * 10 ** -4, 2.60208205 * 10 ** -4, 1.30104102 * 10 ** -4, -1.96929513, 0.96981555)

    while True:
        samples, read = original()
        writetofile(calculatefilter(samples), read)                      # Calculate the filter and write it back to the file
        if read < original.hop_size:
            break

    aubio.sink.close(writetofile)

def bandpassfilter(inputfile, outputlow):
    original = aubio.source(inputfile)                          # Open the original file
    samplerate = original.samplerate                              # get samplerate for output file
    writetofile = aubio.sink(outputlow, samplerate)            # Create Output sink

    # Biquad Filter as Band-Pass-Filter (Combined Low-Pass-Filter and High-Pass-Filter for a better function
    # Low-Pass-Filter
    # Center Frequency 6000
    # Samplerate 41000
    # Q 0.7
    # High-Pass-Filter
    # Center Frequency 200
    # Samplerate 41000
    # Q 0.7
    calculatelowfilter = aubio.digital_filter(3)
    calculatelowfilter.set_biquad(0.12556056, 0.25112113, 0.12556056, -0.77321399, 0.27545624)
    calculatehighfilter = aubio.digital_filter(3)
    calculatehighfilter.set_biquad(0.97834987, -1.95669974, 0.97834987, -1.95624013, 0.95715934)

    while True:
        samples, read = original()
        lowresult = calculatelowfilter(samples)                                # Calculate the Low-Pass-Filter
        writetofile(calculatehighfilter(lowresult), read)                      # Calculate the High-Pass-Filter and write it back to the file
        if read < original.hop_size:
            break

    aubio.sink.close(writetofile)

def highpassfilter(inputfile, outputlow):
    original = aubio.source(inputfile)                          # Open the original file
    samplerate = original.samplerate                              # get samplerate for output file
    writetofile = aubio.sink(outputlow, samplerate)            # Create Output sink

    # Biquad Filter as high-Pass-Filter
    # Center Frequency 6000
    # Samplerate 41000
    # Q 0.7
    calculatefilter = aubio.digital_filter(3)
    calculatefilter.set_biquad(0.51216756, -1.02433511, 0.51216756, -0.77321399, 0.27545624)

    while True:
        samples, read = original()
        writetofile(calculatefilter(samples), read)                      # Calculate the filter and write it back to the file
        if read < original.hop_size:
            break

    aubio.sink.close(writetofile)


if __name__ == '__main__':
    musicpath = os.getcwd()+"\\Musik"                         #Set Path to musicfiles

    orig_stdout = sys.stdout                                #List all Songs from folder Musik
    f = open('Song.txt', 'w')
    sys.stdout = f
    print(os.listdir(musicpath))                            #Write it into Song.txt
    sys.stdout = orig_stdout
    f = open('Song.txt', 'r')
    txt = f.readline()
    txtcontent = ""
    f.close()
    for i in range(0, len(txt)):
        if i != 0 and i != len(txt)-2:
            txtcontent = txtcontent+txt[i]
    os.remove('Song.txt')
    txtcontent = txtcontent.replace("'", "")
    txtcontent = txtcontent.replace(", ","\n")
    p = open('Songs.txt', 'w')
    p.write(txtcontent)
    p.close()
    p = open('Songs.txt', 'r')

    os.chdir(musicpath)                                     #Change working directory for filters
    while True:
        musicnametemp = p.readline()                          #Read lines in Songs.txt
        if musicnametemp == "":                               #If p.readline is empty exit while
            break
        musicname = ""
        for i in range(0, len(musicnametemp)):
            if i < len(musicnametemp)-5:
                musicname = musicname+musicnametemp[i]
        inputfile = musicname+'.wav'
        outputlowpass = musicname+' lowpass.wav'
        outputlowpasstemp1 = musicname+' lowpasstemp1.wav'
        outputlowpasstemp2 = musicname+' lowpasstemp2.wav'
        outputbandpass = musicname+' bandpass.wav'
        outputbandpasstemp1 = musicname+' bandpasstemp1.wav'
        outputbandpasstemp2 = musicname+' bandpasstemp2.wav'
        outputhighpass = musicname+' highpass.wav'
        outputhighpasstemp1 = musicname+' highpasstemp1.wav'
        outputhighpasstemp2 = musicname+' highpasstemp2.wav'

        #bpmdetection(inputfile)
        lowpassfilter(inputfile, outputlowpass)                                 # Cascading 4 Biquad Low-Pass-Filter to get a sharp cut
        lowpassfilter(outputlowpass, outputlowpasstemp1)
        lowpassfilter(outputlowpasstemp1, outputlowpasstemp2)
        lowpassfilter(outputlowpasstemp2, outputlowpass)
        os.remove(musicname+' lowpasstemp1.wav')
        os.remove(musicname+' lowpasstemp2.wav')

        bandpassfilter(inputfile, outputbandpass)                               # Cascading 4 Biquad Band-Pass-Filter to get a sharp cut
        bandpassfilter(outputbandpass, outputbandpasstemp1)
        bandpassfilter(outputbandpasstemp1, outputbandpasstemp2)
        bandpassfilter(outputbandpasstemp2, outputbandpass)
        os.remove(musicname+' bandpasstemp1.wav')
        os.remove(musicname+' bandpasstemp2.wav')

        highpassfilter(inputfile, outputhighpass)                                # Cascading 4 Biquad High-Pass-Filter to get a sharp cut
        highpassfilter(outputhighpass, outputhighpasstemp1)
        highpassfilter(outputhighpasstemp1, outputhighpasstemp2)
        highpassfilter(outputhighpasstemp2, outputhighpass)
        os.remove(musicname+' highpasstemp1.wav')
        os.remove(musicname+' highpasstemp2.wav')                            #Todo: Schöner machen

        shutil.move(outputlowpass, '../Musikgefiltert')                         #Move filtered files to folder Musikgefiltert
        shutil.move(outputbandpass, '../Musikgefiltert')
        shutil.move(outputhighpass, '../Musikgefiltert')

    p.close()
    os.chdir('../')                                                             #Change directory back to the old folder
    os.remove('Songs.txt')                                                      #Clean environment