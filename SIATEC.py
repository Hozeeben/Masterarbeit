import sys
import os.path
import numpy as np
from mido import MidiFile

def SIATEC(track):
    itteration = 0
    note = 0
    while itteration < len(track):
        if track[itteration] == ' ':
            note += 1

    # ToDo: ab hier dann mit plt und meshgrid rummspielen


if __name__ == '__main__':
    tempsting = 'note='
    stringlength = len(tempsting)
    normalstdout = sys.stdout
    f = open('SIATEC.txt', 'w')
    sys.stdout = f
    filename = 'beethoven_ode_to_joy.mid'                                   # ToDo: Variabel machen
    midi_file = MidiFile(filename)

    for i, track in enumerate(midi_file.tracks):
        sys.stdout.write('=== Track {}\n'.format(i))
        for message in track:
            sys.stdout.write('  {!r}\n'.format(message))

    sys.stdout = normalstdout
    f.close()
    f = open('MIDIMatrix.txt', 'r')
    p = open('MusikstückSIATEC.txt', 'w')
    writenote = ''
    while True:                                                                     # Create .txt with only Notenr.
        nextline = f.readline()
        if nextline == "":
            break
        if nextline.find('<meta message end_of_track') != -1:
            if writenote != '':
                p.write(writenote + '\n')
                writenote = ''
        if nextline.find('<message note_on') != -1:
            startnote = nextline.find('note=')
            for i in range(0, 3):
                if nextline[startnote + stringlength + i] == ' ':
                    break
                writenote = writenote + nextline[startnote + stringlength + i]
            writenote = writenote + ' '
    p.close()
    f.close()

    f = open('MusikstückSIATEC.txt', 'r')
    e = open('Ergebnis Patternsuche SIATEC.txt', 'w')
    while True:
        track = f.readline()
        if track == '':
            break
        SIATEC(track)

    f.close()
    e.close()
