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
    PatternSearch(notematrix, matrixindize)
    return notematrix

def PatternSearch(notematrix, matrixindize):
    xindize = 1
    yindize = 1
    print(matrixindize)
    while True:
        if yindize == matrixindize:
            break
        if notematrix[0][yindize] == notematrix[xindize][0]:
            if yindize != 1:
                notematrix[xindize][yindize] = notematrix[xindize-1][yindize-1] + 1
            else:
                notematrix[xindize][yindize] = 1
        xindize += 1
        #print(xindize)
        if xindize == matrixindize:
            yindize += 1
            xindize = yindize
    return notematrix


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
    e = open('Ergebnis Patternsuche Matrix.txt', 'w')
    nroftracks = 1
    sys.stdout = e
    write = 0
    x = 0
    y = 0
    zeilenstring = ''
    while True:
        track = f.readline()
        if track == '':
            break
        print('===Track Nr. ', nroftracks, '===')
        notematrix = PatternsearchPreperation(track)
        for y in range(0, np.size(notematrix,0)):
            for x in range(0, np.size(notematrix, 1)):
                if x == y:
                    zeilenstring = zeilenstring + ' ' + '0'
                else:
                    zeilenstring=zeilenstring + ' ' + str(notematrix[y][x])
            print(zeilenstring)

        #print(notematrix)
        nroftracks += 1
    f.close()
    # ToDO: Ansicht in .txt verbessern um zu Kontrollieren ob Korrekt berechnet