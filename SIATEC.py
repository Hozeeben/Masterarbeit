import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt
from mido import MidiFile

def SIATECOLD(notey, timex):
    notematrix = [[[]]]                                  # weird Array because Python sucks
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

def SIATEC(notey, timex):
    notearray = []
    position = []
    tracklen = len(notey)
    Gausssum = 1
    zaehler = 0
    vektorinformation = [0]
    vektorinformation.append(0)
    while len(notearray) < ((tracklen*(tracklen+1)/2)-tracklen):
        vektorinformation[0] = int(notey[Gausssum] - notey[zaehler])
        vektorinformation[1] = int(timex[Gausssum] - timex[zaehler])
        notearray.append(', '.join(str(x) for x in vektorinformation))
        position.append(str(Gausssum) + ',' + str(zaehler))
        if len(notearray) == (Gausssum*(Gausssum+1)/2):
            Gausssum += 1
            zaehler = 0
        else:
            zaehler += 1
    notearray, position = Quicksort(0, len(notearray)-1, notearray, position)
    for i in range(0, len(notearray)-1):
        print(notearray[i])
    #print(position)
    return
    # ToDo: ab hier dann mit plt und meshgrid rummspielen

def Quicksort(left, right, notearray, position):
    if len(notearray) <= 1:
        return notearray, position
    smallernote = []
    biggernote = []
    smallerposition = []
    biggerposition = []
    informationleft = []
    informationright = []
    informationpivot = []
    informationpivot = notearray[right].split(',')
    informationpivot[0], informationpivot[1] = int(informationpivot[0]), int(informationpivot[1])
    while True:
        informationleft = notearray[left].split(',')
        informationleft[0], informationleft[1] = int(informationleft[0]), int(informationleft[1])
        informationright = notearray[right].split(',')
        informationright[0], informationright[1] = int(informationright[0]), int(informationright[1])
        if informationleft[0] < informationpivot[0]:                    # left is smaller than pivot -> index + 1
            smallernote.append(notearray[left])
            smallerposition.append(position[left])
            left += 1
            if left > right:
                notearrayleft, positionleft = Quicksort(0, len(smallernote) - 1, smallernote, smallerposition)
                notearrayright, positionright = Quicksort(0, len(biggerposition) - 1, biggernote, biggerposition)
                break
        else:
            if informationleft[0] > informationpivot[0] or informationleft[0] == informationpivot[0] and informationleft[1] >= informationpivot[1]:     # left is bigger than pivot -> beginn search for bigger element
                if informationright[0] > informationpivot[0]:
                    biggernote.insert(0, notearray[right])
                    biggerposition.insert(0, position[right])
                    right -= 1
                elif informationright[0] < informationpivot[0] or informationright[0] == informationpivot[0] and informationright[1] <= informationpivot[1]:
                    if right == left:
                        biggernote.insert(0, notearray[left])
                        biggerposition.insert(0, position[left])
                    else:
                        smallernote.append(notearray[right])
                        smallerposition.append(position[right])
                        biggernote.insert(0, notearray[left])
                        biggerposition.insert(0, position[left])
                    left += 1
                    right -= 1
                    if left > right:
                        notearrayleft, positionleft = Quicksort(0, len(smallernote) - 1, smallernote, smallerposition)
                        notearrayright, positionright = Quicksort(0, len(biggerposition) - 1, biggernote, biggerposition)
                        break
                else:
                    biggernote.insert(0, notearray[right])
                    biggerposition.insert(0, position[right])
                    right -= 1
            else:
                left += 1
    notearray = notearrayleft+notearrayright
    position = positionleft+positionright

    return notearray, position


if __name__ == '__main__':
    normalstdout = sys.stdout
    #filename = 'beethoven_ode_to_joy.mid'                                   # ToDo: Variabel machen
    f = open('OneRepublic - If I Lose Myself(original).txt', 'r')
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
