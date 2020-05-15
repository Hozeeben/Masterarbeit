import sys
import timeit
from mido import MidiFile

def Patternsearchpreperation(track):
    patternlist = []
    positionofpattern = []
    patternlengthinnumber = []
    maxpatternlength = len(track)//2                                                #Get longest possible repetetive pattern
    for j in range(maxpatternlength, 2, -1):                                        #-1 because last sign is a ' '
        Patternsearch(track, j, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber, 0)
    for i in range(0, len(positionofpattern)):
        positionofpattern[i] += 1
    ChangeNumbersToNotes(patternlist)
    return patternlist, patternlengthinnumber, positionofpattern

def Patternsearch(track, patternlength, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber, position):
    while True:
        if position + patternlength > len(track):
            return patternlist, positionofpattern, patternlengthinnumber
        else:
            write = True
            difference = 0
            foundpattern = ''
            foundpatternlength = 0
            originalpattern = ''
            startindex = 0
            vertical = 0
            verticalaxis = 0
            for k in range(position + patternlength, len(track)):
                if k + patternlength - foundpatternlength > len(track):
                    break
                if k + 2 < len(track):
                    x = track[position + foundpatternlength] - track[k]                                 #Check if difference is correct for the next 3 notes (Keychange)
                    y = track[position + 1 + foundpatternlength] - track[k+1]
                    z = track[position + 2 + foundpatternlength] - track[k+2]
                    if x == y and x == z:
                        difference = x

                    verticalaxis = int(abs((track[position + foundpatternlength] - track[k])/2))                           # Check if difference is correct for the next 3 notes (vertical change)
                    verticalaxisnextnote = int(abs((track[position + foundpatternlength + 1] - track[k + 1])/2))
                    verticalaxisnextnextnote = int(abs((track[position + foundpatternlength + 2] - track[k + 2])/2))
                    if track[position + foundpatternlength] < track[k]:
                        verticalaxis = track[position + foundpatternlength] + verticalaxis
                        verticalaxisnextnote = track[position + foundpatternlength + 1] + verticalaxisnextnote
                        verticalaxisnextnextnote = track[position + foundpatternlength + 2] + verticalaxisnextnextnote
                    else:
                        verticalaxis = track[k] + verticalaxis
                        verticalaxisnextnote = track[k + 1] + verticalaxisnextnote
                        verticalaxisnextnextnote = track[k + 2] + verticalaxisnextnextnote
                    if verticalaxis == verticalaxisnextnote and verticalaxis == verticalaxisnextnextnote:
                        vertical = 3
                if track[position + foundpatternlength] == track[k]:                                    #Same Pattern
                    foundpattern = foundpattern + ' ' + str(track[k])
                    originalpattern = originalpattern + ' ' + str(track[position+foundpatternlength])
                    foundpatternlength += 1
                    startindex = k - foundpatternlength
                elif track[position + foundpatternlength] - track[k] == difference:                     #Keychange
                    foundpattern = foundpattern + ' ' + str(track[k])
                    originalpattern = originalpattern + ' ' + str(track[position+foundpatternlength])
                    foundpatternlength += 1
                    startindex = k - foundpatternlength
                elif vertical > 0:                                                                      #verticalChange
                    foundpattern = foundpattern + ' ' + str(track[k])
                    originalpattern = originalpattern + ' ' + str(track[position + foundpatternlength])
                    foundpatternlength += 1
                    startindex = k - foundpatternlength
                    vertical -= 1
                else:
                    foundpatternlength = 0
                    foundpattern = ''
                    originalpattern = ''
                if foundpatternlength == patternlength:
                    startindex += 1
                    if len(patternlist) != 0:
                        for a in range(0, len(patternlist)):
                            if startindex in range(positionofpattern[a], positionofpattern[a] + patternlengthinnumber[a]-1) or startindex + patternlength - 1 in range(positionofpattern[a], positionofpattern[a] + patternlengthinnumber[a]-1):
                                write = False
                                break
                    if write == False:
                        write = True
                        continue
                    else:
                        patternlist.append(originalpattern)
                        positionofpattern.append(position)
                        patternlengthinnumber.append(patternlength)
                        patternlist.append(foundpattern)
                        positionofpattern.append(k - patternlength + 1)
                        patternlengthinnumber.append(patternlength)
                        originalpattern = ''
                        foundpattern = ''
                        difference = 0
                        foundpatternlength = 0
            position += 1
            #Patternsearch(track, patternlength, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber, position + 1)
    #return patternlist, positionofpattern, patternlengthinnumber

def ChangeNumbersToNotes(patternlist):
    for i in range(0, len(patternlist)):
        pattern = patternlist[i]
        itteration = 1
        notestemp = ''
        noteswrite = ''
        while itteration < len(pattern):
            if pattern[itteration] != ' ':
                notestemp = notestemp + pattern[itteration]
            if pattern[itteration] == ' ' or itteration == len(pattern)-1:
                noteinint = int(notestemp)
                notestemp = ''
                oktave = (noteinint//12)-1
                note = noteinint%12
                oktave = str(oktave)
                if note == 0:
                    noteswrite = noteswrite + 'C' + oktave + ' '
                elif note == 1:
                    noteswrite = noteswrite + 'CIS' + oktave + ' '
                elif note == 2:
                    noteswrite = noteswrite + 'D' + oktave + ' '
                elif note == 3:
                    noteswrite = noteswrite + 'DIS' + oktave + ' '
                elif note == 4:
                    noteswrite = noteswrite + 'E' + oktave + ' '
                elif note == 5:
                    noteswrite = noteswrite + 'F' + oktave + ' '
                elif note == 6:
                    noteswrite = noteswrite + 'FIS' + oktave + ' '
                elif note == 7:
                    noteswrite = noteswrite + 'G' + oktave + ' '
                elif note == 8:
                    noteswrite = noteswrite + 'GIS' + oktave + ' '
                elif note == 9:
                    noteswrite = noteswrite + 'A' + oktave + ' '
                elif note == 10:
                    noteswrite = noteswrite + 'AIS' + oktave + ' '
                elif note == 11:
                    noteswrite = noteswrite + 'B' + oktave + ' '

            patternlist[i] = noteswrite
            itteration += 1
    return patternlist


if __name__ == '__main__':
    timestart = timeit.default_timer()
    tempsting = 'note='
    stringlength = len(tempsting)
    normalstdout = sys.stdout
    f = open('MIDIString.txt', 'w')
    sys.stdout = f
    filename = 'beethoven_ode_to_joy.mid'                                   # ToDo: Variabel machen
    midi_file = MidiFile(filename)

    for i, track in enumerate(midi_file.tracks):
        sys.stdout.write('=== Track {}\n'.format(i))
        for message in track:
            sys.stdout.write('  {!r}\n'.format(message))

    sys.stdout = normalstdout
    f.close()
    f = open('DarudeSandstormPseudoMIDITest.txt', 'r')
    e = open('Ergebnis Patternsuche String.txt', 'w')
    sys.stdout = e
    writenote = ''
    track = []
    nroftracks = 1
    while True:                                                             #Create .txt with only Notenr. and Time its played
        nextline = f.readline()
        if nextline == "":
            break
        if nextline.find('<meta message end_of_track') != -1:
            if len(track) > 0:
                pattern, length, noteintrack = Patternsearchpreperation(track)
                print('===Track Nr. ', nroftracks, '===')
                for itteration in range(0, len(pattern)):
                    print('Pattern: ', pattern[itteration], '\nLänge des gefundenen Pattern: ',
                          length[itteration], '\nStelle im Musikstück: ', noteintrack[itteration], '\n')
                nroftracks += 1
        if nextline.find('<message note_on') != -1:
            startnote = nextline.find('note=')
            for i in range(0, 2):
                if nextline[startnote+stringlength+i] == ' ':
                    break
                writenote = writenote+nextline[startnote+stringlength+i]
            track.append(int(writenote))
            writenote = ''
    timeend = timeit.default_timer()
    totaltime = timeend - timestart
    e.write(str(totaltime) + ' sec')
    sys.stdout = normalstdout
    f.close()
    e.close()