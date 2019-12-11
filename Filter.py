#! /usr/bin/env python

import sys, os.path
import aubio
from numpy import zeros, log10, vstack
import matplotlib.pyplot as plt

def bpmdetection(inputfile):
    print('Hello Function')
def lowpassfilter(inputfile, outputlow):
    original = aubio.source(inputfile)                          # Open the original file
    samplerate=original.samplerate                              # get samplerate for output file
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
    samplerate=original.samplerate                              # get samplerate for output file
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
    samplerate=original.samplerate                              # get samplerate for output file
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
    inputfile = 'KIRA New World.wav'                                        # ToDo: Variabel gestalten
    outputlowpass = 'KIRA New World lowpass.wav'
    outputlowpasstemp1 = 'KIRA New World lowpasstemp1.wav'
    outputlowpasstemp2 = 'KIRA New World lowpasstemp2.wav'
    outputbandpass = 'KIRA New World bandpass.wav'
    outputbandpasstemp1 = 'KIRA New World bandpasstemp1.wav'
    outputbandpasstemp2 = 'KIRA New World bandpasstemp2.wav'
    outputhighpass = 'KIRA New World highpass.wav'
    outputhighpasstemp1 = 'KIRA New World highpasstemp1.wav'
    outputhighpasstemp2 = 'KIRA New World highpasstemp2.wav'

    bpmdetection(inputfile)
    lowpassfilter(inputfile, outputlowpass)                                 # Cascading 4 Biquad Low-Pass-Filter to get a sharp cut
    lowpassfilter(outputlowpass, outputlowpasstemp1)
    lowpassfilter(outputlowpasstemp1, outputlowpasstemp2)
    lowpassfilter(outputlowpasstemp2, outputlowpass)
    os.remove('KIRA New World lowpasstemp1.wav')
    os.remove('KIRA New World lowpasstemp2.wav')

    bandpassfilter(inputfile, outputbandpass)                               # Cascading 4 Biquad Band-Pass-Filter to get a sharp cut
    bandpassfilter(outputbandpass, outputbandpasstemp1)
    bandpassfilter(outputbandpasstemp1, outputbandpasstemp2)
    bandpassfilter(outputbandpasstemp2, outputbandpass)
    os.remove('KIRA New World bandpasstemp1.wav')
    os.remove('KIRA New World bandpasstemp2.wav')

    highpassfilter(inputfile, outputhighpass)                                # Cascading 4 Biquad High-Pass-Filter to get a sharp cut
    highpassfilter(outputhighpass, outputhighpasstemp1)
    highpassfilter(outputhighpasstemp1, outputhighpasstemp2)
    highpassfilter(outputhighpasstemp2, outputhighpass)
    os.remove('KIRA New World highpasstemp1.wav')
    os.remove('KIRA New World highpasstemp2.wav')                            #Todo: Schöner machen