import sys
import os.path
import numpy as np
from mido import MidiFile

def PatternsearchPreperation(track):
    notecount = 0
    itteration = 0
    tempnote = ''
    while itteration < len(track):
        if track[itteration] == ' ':
            notecount += 1
        itteration += 1
    notecount += 1                                                                  # Because [0][0] is not usable
    notematrix = np.zeros((notecount, notecount))
    itteration = 0
    matrixindize = 1
    while itteration < len(track):
        if track[itteration] == ' ':
            x = int(tempnote)
            notematrix[0][matrixindize] = x
            notematrix[matrixindize][0] = x
            matrixindize += 1
            tempnote = ''
        tempnote = tempnote + track[itteration]
        itteration += 1
    print(notematrix)

if __name__ == '__main__':
    tempsting = 'note='
    stringlength = len(tempsting)
    normalstdout = sys.stdout
    f = open('MIDIMatrix.txt', 'w')
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
    p = open('MusikstückMatrix.txt', 'w')
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
            for i in range(0, 2):
                if nextline[startnote + stringlength + i] == ' ':
                    break
                writenote = writenote + nextline[startnote + stringlength + i]
            writenote = writenote + ' '
    p.close()
    f.close()

    f = open('MusikstückMatrix.txt', 'r')
    while True:
        track = f.readline()
        if track == '':
            break
        PatternsearchPreperation(track)

    f.close()
