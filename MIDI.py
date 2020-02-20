import sys
import os.path
from mido import MidiFile

def normalpatternsearchpreperation(Inputfile):
    patternlist = []
    positionofpattern = []
    patternlengthinnumber = []
    f=open(Inputfile, 'r')

    while True:
        track=f.readline()
        if track=='':
            break
        maxpatternlength=0
        for i in range(0, len(track)):                      #Get longest possible repetetive pattern
            if track[i]==' ':
                maxpatternlength=maxpatternlength+1
        maxpatternlength=maxpatternlength//2
        print(maxpatternlength)
        nextnote = 0
        for j in range(0, len(track)-1):                                        #-1 because last sign is a ' '
            print('Momentan an Pos ',j)
            itteration = 0
            if nextnote > 0:
                nextnote -= 1
                continue
            else:
                patternsearch(track, 1, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber, j)
            while True:
                itteration += 1
                if track[j+itteration] == ' ':
                    nextnote += 1
                    break
                nextnote += 1
    return patternlist

def patternsearch(track, patternlength, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber, position):
    print('Called Patternsearch')
    if patternlength > maxpatternlength:
        print('Finished Patternsearch patternlength>maxlength')
        return patternlist
    elif position+patternlength>len(track):
        print('Finished Patternsearch because String would go out of bound')
        return patternlist, positionofpattern, patternlengthinnumber
    else:
        patternsearch(track, patternlength+1, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber,
                      position)
        stringlength=len(track)
        patternlengthtemp=patternlength
        patternstring = ''
        whitespaces = 0
        itteration = 0
        occurence = 0
        while True:
            if len(track) <= position+itteration:
                return patternlist, positionofpattern, patternlengthinnumber
            if track[position+itteration] == ' ':                                    # Write Patternstring into variable
                whitespaces += 1
            if whitespaces == patternlength:
                break
            patternstring = patternstring+track[position+itteration]
            itteration += 1
        print('Patternstring:',patternstring)
        write = True
        stop = 0
        writefirstoccurence = True
        while True:                                                                 # Write all patterns in a list
            occurence = track.find(patternstring, occurence, stringlength)          # List is splitted into patternstring,
            print('Occurence:',occurence)
            if occurence == -1:                                                     # position of the pattern and length in int
                break
            if occurence != -1:
                for i in range(occurence, occurence+len(patternstring)):
                    if len(positionofpattern) == 0:
                        write = True
                        print('Case 4')
                        break
                    for j in range(0, len(positionofpattern)):
                        print('Patternposition:',positionofpattern[j])
                        print('i:',i)
                        print('Max Ausbreitung:',positionofpattern[j]+patternlengthinnumber[j])
                        if i in range (positionofpattern[j], positionofpattern[j]+patternlengthinnumber[j]):
            # ToDo: patternlengthinnumber wird nicht in Anzahl Stringposition gerechnet->Zwischenpattern werden erkannt
                        #if positionofpattern[j]==i:
                            write = False
                            print('case 1')
                            stop = 1
                            break
                        else:
                            write = True
                            print('case 2')
                    if stop == 1:
                        stop = 0
                        break
            if occurence == position:
                write = False
                print('case 3')
            if write:
                if writefirstoccurence:
                    patternlist.append(patternstring)
                    positionofpattern.append(position)
                    patternlengthinnumber.append(patternlength)
                    writefirstoccurence = False
                patternlist.append(patternstring)
                positionofpattern.append(occurence)
                patternlengthinnumber.append(patternlength)
            occurence += 1
            print(patternlist)
        print('Finished Patternsearch normaly')
        return patternlist, positionofpattern, patternlengthinnumber






if __name__ == '__main__':
    tempsting = 'note='
    stringlength = len(tempsting)
    normalstdout=sys.stdout
    f=open('MIDI.txt', 'w')                                         # ToDo: Variabel machen
    sys.stdout=f
    filename = 'bach.mid'
    midi_file = MidiFile(filename)

    for i, track in enumerate(midi_file.tracks):
        sys.stdout.write('=== Track {}\n'.format(i))
        for message in track:
            sys.stdout.write('  {!r}\n'.format(message))

    sys.stdout=normalstdout
    f.close()
    f=open('MIDI.txt','r')
    p=open('Musikstück.txt', 'w')
    writenote=''
    while True:                                                             #Create .txt with only Notenr. and Time its played
        nextline=f.readline()
        if nextline=="":
            break
        if nextline.find('<meta message end_of_track')!=-1:
            if writenote!='':
                p.write(writenote+'\n')
                writenote=''
            #p.write(writetime + '\n')
        if nextline.find('<message note_on')!=-1:
            startnote=nextline.find('note=')
            #starttime=nextline.find('time=')
            for i in range(0,2):
                if nextline[startnote+stringlength+i]==' ':
                    break
                writenote=writenote+nextline[startnote+stringlength+i]
            writenote = writenote + ' '
            #for i in range(0,6):
            #    if nextline[starttime + stringlength + i] == '>':
            #        break
            #    writetime = writetime + nextline[starttime + stringlength + i]

    p.close()
    f.close()
    finalpattern = normalpatternsearchpreperation('Musikstücktemp2.txt')
    print(finalpattern)
    # ToDo: Jeden Track einzeln aus Datei lesen und verarbeiten
    # ToDo: Index von Anfang der Pattern ausgeben
    # ToDo: Für jeden Track eigene Liste