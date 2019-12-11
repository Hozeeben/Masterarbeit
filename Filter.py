#! /usr/bin/env python

import sys, os.path
import aubio
from numpy import zeros, log10, vstack
import matplotlib.pyplot as plt

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

    # Biquad Filter as Band-Pass-Filter
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

def highpassfilter(inputfile, outputlow):
    original = aubio.source(inputfile)                          # Open the original file
    samplerate=original.samplerate                              # get samplerate for output file
    writetofile = aubio.sink(outputlow, samplerate)            # Create Output sink

    # Biquad Filter as high-Pass-Filter
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


if __name__ == '__main__':
    inputfile = 'KIRA New World.wav'
    outputlowpass = 'KIRA New World lowpass.wav'
    outputlowpasstemp1 = 'KIRA New World lowpasstemp1.wav'
    outputlowpasstemp2 = 'KIRA New World lowpasstemp2.wav'
    outputbandpass = 'KIRA New World bandpass.wav'
    outputbandpasstemp1 = 'KIRA New World bandpasstemp1.wav'
    outputbandpasstemp2 = 'KIRA New World bandpasstemp2.wav'
    outputhighpass = 'KIRA New World highpass.wav'
    outputhighpasstemp1 = 'KIRA New World highpasstemp1.wav'
    outputhighpasstemp2 = 'KIRA New World highpasstemp2.wav'


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
    os.remove('KIRA New World highpasstemp2.wav')