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
    difference = []
    for i in range(0, len(track)-1):
        difference.append(track[i]-track[i+1])
    while True:                                                                     # Add Patterns here
        if yindize >= len(track)+1:                                                 # In-Range checks
            break
        if xindize >= len(track)+1:
            yindize += 1
            xindize = yindize
            continue
        if xindize <= yindize:
            xindize += 1
            continue
        if notematrix[yindize, xindize] == -1:
            notematrix[yindize, xindize] = notematrix[yindize - 1, xindize - 1] + 1
        if notematrix[0, xindize] == notematrix[yindize, 0]:                        #Patternclass=same
            if yindize != 1:
                notematrix[yindize, xindize] = notematrix[yindize-1, xindize-1] + 1
            else:
                notematrix[yindize, xindize] = 1
            xindize += 1
            continue
        if xindize + 1 < np.size(notematrix, 1):                                    #Patternclass=Keychange
            if difference[yindize-1] == notematrix[0, xindize] - notematrix[0, xindize + 1]:
                if yindize != 1:
                    notematrix[yindize, xindize] = notematrix[yindize - 1, xindize - 1] + 1
                else:
                    notematrix[yindize, xindize] = 1
                notematrix[yindize + 1, xindize + 1] = -1
        xindize += 1


    for y in range(np.size(notematrix, 0)-1, 0, -1):
        patternstring = ''
        for x in range(np.size(notematrix, 1)-1, 0, -1):
            if x < y:
                continue
            elif x == y:
                notematrix[y, x] = 0
            elif notematrix[y, x] > 2:
                xtemp = x
                ytemp = y
                patternlength = notematrix[y, x]
                xtemp = xtemp-(patternlength-1)
                ytemp = ytemp-(patternlength-1)
                yxtemp = str(ytemp) + ' ' + str(xtemp)
                if yxtemp not in foundpatternindize:
                    foundpatternlength.append(patternlength)
                    foundpatternindize.append(yxtemp)
                    patternlength = 0
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
    f = open('MIDIMatrixTemp.txt', 'r')
    e = open('Ergebnis Patternsuche Matrix.txt', 'w')
    writenote = ''
    track = []
    nroftracks = 1
    while True:                                                                     # Create .txt with only Notenr.
        nextline = f.readline()
        if nextline == "":
            break
        if nextline.find('<meta message end_of_track') != -1:
            if len(track) != 0:
                notematrix, patternlength, indize = PatternSearch(track)
                sys.stdout = e
                print('===Track Nr. ', nroftracks, '===')
                for i in range(0, len(indize)):  # ToDo: nicht alle Patternergebnisse mit in .txt übernehmen
                    patternstring1 = ''
                    patternstring2 = ''
                    indizes = indize[i]
                    tempstr = indizes.split()
                    ytemp = int(float(tempstr[0]))
                    xtemp = int(float(tempstr[1]))
                    patternlengthtmp = int(patternlength[i])
                    if ytemp + patternlengthtmp > xtemp:
                        continue
                    for j in range(0, patternlengthtmp):
                        patternstring1 = patternstring1 + ' ' + str(notematrix[ytemp + j, 0])
                        patternstring2 = patternstring2 + ' ' + str(notematrix[xtemp + j, 0])
                    print('\nGefundene Pattern: ' + patternstring1 + ', ' + patternstring2 + '\nNoten im Lied: ' + str(ytemp) + ', ' + str(xtemp)
                          + '\nLänge des Patterns: ' + str(patternlengthtmp))
                sys.stdout = normalstdout
                nroftracks += 1
                track = []
        if nextline.find('<message note_on') != -1:
            startnote = nextline.find('note=')
            for i in range(0, 3):
                if nextline[startnote + stringlength + i] == ' ':
                    break
                writenote = writenote + nextline[startnote + stringlength + i]
            track.append(int(writenote))
            writenote = ''
    f.close()
    e.close()

    # ToDo: Prints im nachhinein checken
    # ToDo: Check ob Indize schon vergeben
    # ToDO: Ansicht in .txt verbessern um zu Kontrollieren ob Korrekt berechnet
    # ToDo: MIDI Notennummern zu Noten machen
