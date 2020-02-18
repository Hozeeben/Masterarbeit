import sys
import os.path
from mido import MidiFile

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
    p=open('Musikstück.txt', 'r')
    i=1
    while True:
        if p.readline()!='':
           print(i)
           i=i+1
        else:
            break

    # ToDo: Jeden Track einzeln aus Datei lesen und verarbeiten
    # ToDo: Index von Anfang der Pattern ausgeben