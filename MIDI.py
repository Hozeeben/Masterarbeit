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
        for j in range(0, len(track)-1):
            patternsearch(track, 1, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber, j)

def patternsearch(track, patternlength, maxpatternlength, patternlist, positionofpattern, patternlengthinnumber, position):
    if patternlength > maxpatternlength:
        return patternlist
    elif position+patternlength>len(track):
        return patternlist
    else:
        stringlength=len(track)
        patternlengthtemp=patternlength
        patternstring = ''
        whitespaces = 0
        itteration = 0
        occurence = 0
        while True:
            if track[position+itteration] == ' ':                                    # Write Patternstring into variable
                whitespaces += 1
            if whitespaces == patternlength:
                break
            patternstring = patternstring+track[position+itteration]

        while occurence != -1:                                                      # Write all patterns in a list
            occurence = track.find(patternstring, occurence+1, stringlength)        # List is splitted into patternstring,
            if occurence != -1:                                                     # position of the pattern and length in int
                # An dieser Stelle ganzen Voraussetzungen wann PAttern NICHT aufgenommen werden müssen
                patternlist.append(patternstring)
                positionofpattern.append(occurence)
                patternlengthinnumber.append(patternlength)






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
    normalpatternsearchpreperation('Musikstück.txt')

    # ToDo: Jeden Track einzeln aus Datei lesen und verarbeiten
    # ToDo: Index von Anfang der Pattern ausgeben