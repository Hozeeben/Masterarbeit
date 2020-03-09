import sys
import os.path
from mido import MidiFile

def Patternsearchpreperation(track):
    patternlist = []
    positionofpattern = []
    patternlengthinnumber = []
    patternlengthinletters = []
    maxpatternlength = len(track)//2                                                #Get longest possible repetetive pattern
    #print(maxpatternlength)
    nextnote = 0
    for j in range(maxpatternlength, 1, -1):                                        #-1 because last sign is a ' '
        Patternsearch(track, j, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber, 0)


    ChangeNumbersToNotes(patternlist)
    return patternlist, patternlengthinnumber, positionofpattern

def Patternsearch(track, patternlength, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber, position):
    if position+patternlength > len(track):
        return patternlist
    else:
        write = True
        writefirstoccurence = False
        foundpattern = ''
        for k in range(position+patternlength+1, len(track)-(patternlength-1)):                                     #Same Pattern is Found
            if track[position] != track[k]:
                continue
            else:
                for a in range(0, len(patternlist)):
                    if position+k in range(positionofpattern[a], positionofpattern[a]+patternlengthinnumber[a]):
                        write = False
                if write is False:
                    write = True
                    continue
                foundpattern = str(track[k])
                for length in range(1, patternlength):
                    if track[position+length] != track[k+length]:
                        foundpattern = ''
                        break
                    if track[position+length] == track[k+length]:
                        foundpattern = foundpattern + ' ' + str(track[k+length])
                        if length+1 == patternlength:
                            if writefirstoccurence is False or len(patternlist) == 0:
                                patternlist.append(foundpattern)
                                positionofpattern.append(position)
                                patternlengthinnumber.append(patternlength)
                                writefirstoccurence = True
                            patternlist.append(foundpattern)
                            positionofpattern.append(position+k)
                            patternlengthinnumber.append(patternlength)
                            k = k+patternlength
                            foundpattern = ''
        Patternsearch(track, patternlength, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber, position + 1)
        return patternlist, positionofpattern, patternlengthinnumber

def ChangeNumbersToNotes(patternlist):
    for i in range(0, len(patternlist)):
        pattern = patternlist[i]
        itteration = 0
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
    f = open('MIDIString.txt', 'r')
    p = open('MusikstückString.txt', 'w')
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
                e = open('Ergebnis Patternsuche String.txt', 'w')
                sys.stdout = e
                print('===Track Nr. ', nroftracks, '===')
                for itteration in range(0, len(pattern)):
                    print('Pattern: ', pattern[itteration], '\nLänge des gefundenen Pattern: ',
                          length[itteration], '\nStelle im Musikstück: ', noteintrack[itteration], '\n')
                nroftracks += 1
                sys.stdout = normalstdout
                e.close()
        if nextline.find('<message note_on') != -1:
            startnote = nextline.find('note=')
            for i in range(0, 2):
                if nextline[startnote+stringlength+i] == ' ':
                    break
                writenote = writenote+nextline[startnote+stringlength+i]
            track.append(int(writenote))
            writenote = ''
    p.close()
    f.close()
    e.close()
    # ToDO: Wenn korrekt auskommentierte prints entfehrnen
