#! /usr/bin/env python

import sys
import os.path
import aubio


def apply_filter2(path, target):
    # open input file, get its samplerate
    s = aubio.source(path)
    samplerate = s.samplerate

    # create an A-weighting filter (Biquad)
    f = aubio.digital_filter(3)
    #f.set_a_weighting(samplerate)
    f.set_biquad(1.00187537, -1.98008047, 0.97848147, -1.98012083, 0.98031648)     #Kombi von 2 FIlter(Lowshelf+Lowpass)

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


    # print some info
    duration = total_frames / float(samplerate)
    input_str = "input: {:s} ({:.2f} s, {:d} Hz)"
    output_str = "output: {:s}, A-weighting filtered ({:d} frames total)"
    print(input_str.format(s.uri, duration, samplerate))
    print(output_str.format(o.uri, total_frames))


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


if __name__ == '__main__':
    input_path='KIRA New World.wav'
    output_path= 'KIRA New World Filtered.wav'
    apply_filter(input_path, output_path)
    #apply_filter2('Temp.wav', output_path)