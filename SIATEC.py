import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt
from mido import MidiFile

def SIATEC(notey, timex):
    notematrix = [[[]]]                                  # 3 dimensions because Python sucks
    temparray = [[]]
    vektor = []
    vektorinformation = [0]
    vektorinformation.append(0)
    for tonote in range(0, len(notey)-1):
        for fromnote in range(0, len(notey)-1):
            if tonote <= fromnote:
                while len(temparray) < len(notey) - 1:
                    vektor.append('0, 0')
                    temparray.append(vektor)
                    vektor = []
                notematrix.append(temparray)
                temparray = []
                break
            else:
                vektorinformation[0] = int(notey[tonote] - notey[fromnote])
                vektorinformation[1] = int(timex[tonote] - timex[fromnote])
                vektor.append(', '.join(str(x) for x in vektorinformation))
                temparray.append(vektor)
                vektor = []
    notematrix.pop(0)
    notematrix.pop(0)

    # Sortieren und dann noch Pattern auslesen x-Achse ist welche Note gerade betrachtet wird und y-Achse zu welcher Note gegangen wird
    # Bsp.: momentane Note     = 0,40
    #       zu Note            = 1,47
    #       Ermittelter Vektor = 1,7
    # print(notematrix[5][3])   Erste Element Zeile, zweite Element Spalte

    plt.scatter(timex, notey)
    plt.show()
    return

    # ToDo: ab hier dann mit plt und meshgrid rummspielen


if __name__ == '__main__':
    normalstdout = sys.stdout
    #filename = 'beethoven_ode_to_joy.mid'                                   # ToDo: Variabel machen
    f = open('OneRepublic - If I Lose Myself.txt', 'r')
    notestring = ''
    timestring = ''
    timex = []
    notey = []
    track = 1
    trackstr = '1'
    while True:
        nextline = f.readline()
        nextline = nextline[:-1]
        if nextline == "":
            track += 1
            trackstr = str(track)
            if len(timex) > 0:
                SIATEC(notey, timex)
                f.seek(0)
                timex = []
                notey = []
            else:
                break
        else:
            tempstring = nextline.split(',')
            if tempstring[2] == trackstr:
                timex.append(int(tempstring[0]))
                notey.append(int(tempstring[1]))

    f.close()
    # LittleTranscriptor nehmen
    # https://www.youtube.com/watch?v=7K4hBdokhbE
    # nochmal mit 2ten monitor
    # jeder strich sind 2 sek keine 4
