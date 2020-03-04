import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt
from mido import MidiFile

def SIATEC(notey, timex):
    plt.scatter(timex, notey)
    plt.show()

    # ToDo: ab hier dann mit plt und meshgrid rummspielen


if __name__ == '__main__':
    tempsting = 'note='
    stringlength = len(tempsting)
    normalstdout = sys.stdout
    filename = 'beethoven_ode_to_joy.mid'                                   # ToDo: Variabel machen
    f = open('Queen.txt', 'r')
    p = open('MusikstückSIATEC.txt', 'w')
    notestring = ''
    timestring = ''
    timex = []
    notey = []
    while True:                                                                     # Create .txt with only Notenr.
        nextline = f.readline()
        if nextline == '':
            SIATEC(notey, timex)
            break
        #if nextline.find('TrkEnd') != -1:                                                 # Class SIATEC
        if nextline.find(' On ') != -1:                                             # Prepare everything vor SIATEC
            for i in range(0, len(nextline)):
                if nextline[i] == ' ':
                    notestart = nextline.find('n=') + 2
                    timex.append(int(int(timestring)//100))
                    timestring = ''
                    for j in range(0, 3):
                        if nextline[notestart+j] == ' ':
                            notey.append(int(notestring))
                            notestring = ''
                            break
                        notestring = notestring + nextline[notestart+j]
                    break
                else:
                    timestring = timestring + nextline[i]

    p.close()
    f.close()
    #plt.scatter(xx,yy)
    #plt.show()

    f = open('MusikstückSIATEC.txt', 'r')
    e = open('Ergebnis Patternsuche SIATEC.txt', 'w')
    #while True:
    #    track = f.readline()
    #    if track == '':
    #        break
    #    SIATEC(track)

    f.close()
    e.close()
    # Mit Programm Midicomp die txt bekommen mit -t für absolute Zeit