import sys
import os.path
from mido import MidiFile

def Patternsearchpreperation(track):
    patternlist = []
    positionofpattern = []
    patternlengthinnumber = []
    patternlengthinletters = []
    maxpatternlength = 0
    for i in range(0, len(track)):                                          #Get longest possible repetetive pattern
        if track[i] == ' ':
            maxpatternlength += 1
    maxpatternlength = maxpatternlength//2
    #print(maxpatternlength)
    nextnote = 0
    for j in range(maxpatternlength, 1, -1):                                        #-1 because last sign is a ' '
        #print('Momentan an Pos ',j)
        itteration = 0
        #if nextnote > 0:
        #    nextnote -= 1
        #    continue
        #else:
        Patternsearch(track, j, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber, patternlengthinletters, 0)
        #while True:
        #    itteration += 1
        #    if track[j+itteration] == ' ':
        #        nextnote += 1
        #        break
        #    nextnote += 1
    for i in range(0, len(positionofpattern)):
        position = 0
        for j in range(0, positionofpattern[i]):
            if track[j] == ' ':
                position += 1
        positionofpattern[i] = position+1
    ChangeNumbersToNotes(patternlist)
    return patternlist, patternlengthinnumber, positionofpattern

def Patternsearch(track, patternlength, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber, patternlengthinletters, position):
    #print('Called Patternsearch')
    patternstring = ''
    whitespaces = 0
    itteration = 0
    while True:  # Write Patternstring into variable
        if len(track) <= position + itteration:
            return patternlist, positionofpattern, patternlengthinnumber, patternlengthinletters
        if track[position + itteration] == ' ':
            whitespaces += 1
        if whitespaces == patternlength:
            break
        patternstring = patternstring + track[position + itteration]
        itteration += 1
    if position+len(patternstring) > len(track):
        #print('Finished Patternsearch because String would go out of bound')
        return patternlist
    else:
        stringlength = len(track)
        occurence = 0
        #print('Patternstring:',patternstring)
        write = True
        stop = 0
        writefirstoccurence = True
        positiontemp = position
        while True:                                                                 # Write all patterns in a list
            occurence = track.find(patternstring, positiontemp, stringlength)          # List is splitted into patternstring,
            #print('Occurence:',occurence, ' From Patternstring:', patternstring)
            if occurence == -1:                                                     # position of the pattern and length in int
                break
            if occurence != -1 and occurence != position:
                for i in range(occurence, occurence+len(patternstring)):
                    if len(positionofpattern) == 0:
                        write = True
                        #print('Case 4')
                        break
                    for j in range(0, len(positionofpattern)):
                        #print('Patternposition:',positionofpattern[j])
                        #print('i:',i)
                        #print('Max Ausbreitung:',positionofpattern[j]+patternlengthinnumber[j])
                        if positionofpattern[j] <= i <= positionofpattern[j]+patternlengthinletters[j] or positionofpattern[j] <= position <= positionofpattern[j]+patternlengthinletters[j]:
                        #if positionofpattern[j]==i:
                            write = False
                            #print('case 1')
                            stop = 1
                            break
                        else:
                            write = True
                    if stop == 1:
                        stop = 0
                        break
            if occurence == position:
                write = False
                #print('case 3')
            if write:
                if writefirstoccurence:
                    patternlist.append(patternstring)
                    positionofpattern.append(position)
                    patternlengthinnumber.append(patternlength)
                    patternlengthinletters.append(len(patternstring))
                    writefirstoccurence = False
                patternlist.append(patternstring)
                positionofpattern.append(occurence)
                patternlengthinnumber.append(patternlength)
                patternlengthinletters.append(len(patternstring))
            positiontemp += 1
            #print(patternlist)
        #print('Finished Patternsearch normaly')
        itteration2 = 0
        nextnote = 0
        while True:
            itteration2 += 1
            if track[position + itteration2] == ' ':
                nextnote += 1
                break
            nextnote += 1
        nextnote += 1
        Patternsearch(track, patternlength, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber,
                      patternlengthinletters,
                      position + nextnote)
        return patternlist, positionofpattern, patternlengthinnumber, patternlengthinletters

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
    while True:                                                             #Create .txt with only Notenr. and Time its played
        nextline = f.readline()
        if nextline == "":
            break
        if nextline.find('<meta message end_of_track') != -1:
            if writenote != '':
                p.write(writenote+'\n')
                writenote = ''
            #p.write(writetime + '\n')
        if nextline.find('<message note_on') != -1:
            startnote = nextline.find('note=')
            #starttime=nextline.find('time=')
            for i in range(0, 2):
                if nextline[startnote+stringlength+i] == ' ':
                    break
                writenote = writenote+nextline[startnote+stringlength+i]
            writenote = writenote + ' '
            #for i in range(0,6):
            #    if nextline[starttime + stringlength + i] == '>':
            #        break
            #    writetime = writetime + nextline[starttime + stringlength + i]
    p.close()
    f.close()
    p = open('MusikstückString.txt', 'r')
    e = open('Ergebnis Patternsuche String.txt', 'w')
    nroftracks = 1
    sys.stdout = e
    while True:
        tracks = p.readline()
        if tracks == '':
            break
        print('===Track Nr. ', nroftracks, '===')
        pattern, length, noteintrack = Patternsearchpreperation(tracks)
        itterations = 0
        while itterations < len(pattern):
            print('Pattern: ',pattern[itterations],'\nLänge des gefundenen Pattern: ', length[itterations], '\nStelle im Musikstück: ', noteintrack[itterations],'\n')
            itterations +=1
        nroftracks += 1
    sys.stdout = normalstdout
    e.close()
    # ToDO: Wenn korrekt auskommentierte prints entfehrnen
