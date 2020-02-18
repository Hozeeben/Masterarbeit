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
    while True:                                                             #Create .txt with only Notenr. and Time its played
        nextline=f.readline()
        if nextline=="":
            break
        #print(nextline.find('<message note on'))
        if nextline.find('<message note_on')!=-1:
            startnote=nextline.find('note=')
            starttime=nextline.find('time=')
            writenote=''
            writetime=''
            for i in range(0,2):
                if nextline[startnote+stringlength+i]==' ':
                    break
                writenote=writenote+nextline[startnote+stringlength+i]
            for i in range(0,6):
                if nextline[starttime + stringlength + i] == '>':
                    break
                writetime = writetime + nextline[starttime + stringlength + i]
            p.write(writenote + ' ')
            p.write(writetime + '\n')
    p.close