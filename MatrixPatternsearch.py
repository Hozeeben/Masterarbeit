import sys
import os.path
import numpy as np
from mido import MidiFile

def PatternSearch(track):
    notematrix = np.zeros((len(track)+1, len(track)+1))                       # Because [0][0] is not usable
    for itteration in range(1, len(track)+1):                                   # initialize Matrix
        notematrix[0, itteration] = track[itteration-1]
        notematrix[itteration, 0] = track[itteration-1]

    foundpatternlength = []
    foundpatternindize = []                                                         # ToDo: Unterteilung der Algorithmen mit Switch Case
    xindize = 1                                                                     # ToDo: Maybe for each Pattern one Matrix (maybe for each one Function)
    yindize = 1
    while True:                                                                     # Add Patterns here
        if yindize == len(track)+1:
            break
        if notematrix[0, xindize] == notematrix[yindize, 0]:                        # Patternclass=same
            if yindize != 1:
                notematrix[yindize, xindize] = notematrix[yindize-1, xindize-1] + 1
            else:
                notematrix[yindize, xindize] = 1
        xindize += 1
        if xindize == len(track)+1:
            yindize += 1
            xindize = yindize


        for y in range(1, np.size(notematrix, 0)):
            patternstring = ''
            for x in range(1, np.size(notematrix, 1)):
                if x < y:
                    continue
                elif x == y:
                    notematrix[y, x] = 0
                elif notematrix[y, x] > 2:
                    xtemp = x
                    ytemp = y
                    patternlength = 0
                    while True:
                        if notematrix[ytemp, xtemp] < 2 or xtemp == len(track) or ytemp == len(track):
                            break
                        patternlength = int(notematrix[ytemp, xtemp])
                        xtemp += 1
                        ytemp += 1
                    yxtemp = str(ytemp) + ' ' + str(xtemp)
                    if yxtemp not in foundpatternindize:
                        foundpatternlength.append(patternlength)
                    foundpatternindize.append(yxtemp)

    return notematrix, foundpatternlength, foundpatternindize



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
    writenote = ''
    track = []
    while True:                                                                     # Create .txt with only Notenr.
        nextline = f.readline()
        if nextline == "":
            break
        if nextline.find('<meta message end_of_track') != -1:
            notematrix, patternlength, indize = PatternSearch(track)
        if nextline.find('<message note_on') != -1:
            startnote = nextline.find('note=')
            for i in range(0, 3):
                if nextline[startnote + stringlength + i] == ' ':
                    break
                writenote = writenote + nextline[startnote + stringlength + i]
            track.append(int(writenote))
    f.close()

    e = open('Ergebnis Patternsuche Matrix.txt', 'w')
    nroftracks = 1
    #sys.stdout = e
    write = 0
    x = 0
    y = 0

    #while True:
    #    track = f.readline()
    #    if track == '':
    #        break
    #    print('===Track Nr. ', nroftracks, '===')

    for i in range(0, len(patternlength)):  # ToDo: nicht alle Patternergebnisse mit in .txt übernehmen
        patternstring = ''
        indize = indize[i]
        tempstr = indize.split()
        ytemp = int(tempstr[0])
        xtemp = int(tempstr[1])
        patternlength = patternlength[i]
        for j in range(0, patternlength):
            patternstring = patternstring + ' ' + str(notematrix[ytemp - patternlength + j, 0])
        print(patternstring)
    nroftracks += 1

    e.close()
    #sys.stdout = normalstdout
    # ToDo: Check ob Indize schon vergeben
    # ToDO: Ansicht in .txt verbessern um zu Kontrollieren ob Korrekt berechnet
    # ToDo: MIDI Notennummern zu Noten machen
