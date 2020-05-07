import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt
from mido import MidiFile

def SIA(notey, timex):
    plt.scatter(timex, notey)
    plt.xlabel('Note in Track')
    plt.ylabel('Notepitch')
    plt.show()
    notearray = []
    position = []
    tracklen = len(notey)
    Gausssum = 1
    zaehler = 0
    vektorinformation = [0]
    vektorinformation.append(0)
    while len(notearray) < ((tracklen*(tracklen+1)/2)-tracklen):                    # Calculation of Vektors
        vektorinformation[0] = int(notey[Gausssum] - notey[zaehler])
        vektorinformation[1] = int(timex[Gausssum] - timex[zaehler])
        notearray.append(', '.join(str(x) for x in vektorinformation))
        position.append(str(Gausssum + 1) + ',' + str(zaehler + 1))
        if len(notearray) == (Gausssum*(Gausssum+1)/2):
            Gausssum += 1
            zaehler = 0
        else:
            zaehler += 1
    notearray, position = Quicksort(0, len(notearray)-1, notearray, position)
    plt.show()
    return notearray, position

def Quicksort(left, right, notearray, position):
    if len(notearray) <= 1:
        return notearray, position
    smallernote = []
    biggernote = []
    smallerposition = []
    biggerposition = []
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
                    if left > right:
                        notearrayleft, positionleft = Quicksort(0, len(smallernote) - 1, smallernote, smallerposition)
                        notearrayright, positionright = Quicksort(0, len(biggerposition) - 1, biggernote, biggerposition)
                        break
                elif informationright[0] < informationpivot[0] or informationright[0] == informationpivot[0] and informationright[1] <= informationpivot[1]:
                    if right == left:
                        biggernote.insert(0, notearray[left])
                        biggerposition.insert(0, position[left])
                        left += 1
                        if left > right:
                            notearrayleft, positionleft = Quicksort(0, len(smallernote) - 1, smallernote, smallerposition)
                            notearrayright, positionright = Quicksort(0, len(biggerposition) - 1, biggernote, biggerposition)
                            break
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
                    if left > right:
                        notearrayleft, positionleft = Quicksort(0, len(smallernote) - 1, smallernote, smallerposition)
                        notearrayright, positionright = Quicksort(0, len(biggerposition) - 1, biggernote, biggerposition)
                        break
            else:
                smallernote.append(notearray[left])
                smallerposition.append(position[left])
                left += 1
                if left > right:
                    notearrayleft, positionleft = Quicksort(0, len(smallernote) - 1, smallernote, smallerposition)
                    notearrayright, positionright = Quicksort(0, len(biggerposition) - 1, biggernote, biggerposition)
                    break
    notearray = notearrayleft+notearrayright
    position = positionleft+positionright

    return notearray, position


if __name__ == '__main__':
    normalstdout = sys.stdout
    #filename = 'beethoven_ode_to_joy.mid'                                   # ToDo: Variabel machen
    f = open('Bild.txt', 'r')
    p = open('Ergebnis Patternsuche SIATEC.txt', 'w')
    sys.stdout = p
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
                print('===Track ' + str(track-1) + '===\n')
                notearray, positionsolution = SIA(notey, timex)
                difference = []
                positiontemp = []
                position = []
                itterator = 0
                patternlength = 0
                patternstart = []
                patternend = []
                same = False
                while itterator < len(notearray) - 1:
                    patterninformation = notearray[itterator].split(', ')
                    nextpatterninformation = notearray[itterator + 1].split(', ')
                    if nextpatterninformation[0] == patterninformation[0] and nextpatterninformation[1] == patterninformation[1]:
                        same = True
                        positiontemp.append(positionsolution[itterator])
                    elif (nextpatterninformation[0] != patterninformation[0] or nextpatterninformation[1] != patterninformation[1]) and same:
                        same = False
                        positiontemp.append(positionsolution[itterator])
                        positiontemp.sort()
                        position.append(positiontemp)
                        positiontemp = []
                    elif (nextpatterninformation[0] != patterninformation[0] or nextpatterninformation[1] != patterninformation[1]) and same is False:
                        del notearray[itterator]
                        del positionsolution[itterator]
                        if len(positiontemp) != 0:
                            positiontemp.sort()
                            position.append(positiontemp)
                            positiontemp = []
                        continue
                    itterator += 1
                if nextpatterninformation[0] != patterninformation[0] or nextpatterninformation[1] != patterninformation[1]:        # Sort out some results
                    del notearray[len(notearray) - 1]
                    itterator = 0
                while itterator < len(notearray) - 1:
                    sort1 = notearray[itterator].split(', ')
                    sort1[0], sort1[1] = int(sort1[0]), int(sort1[1])
                    sort2 = notearray[itterator + 1].split(', ')
                    sort2[0], sort2[1] = int(sort2[0]), int(sort2[1])
                    if sort1[0] == sort2[0] and sort1[1] == sort2[1]:
                        del notearray[itterator+1]
                        continue
                    itterator += 1

                itterator = 0
                while itterator < len(position):
                    sort1 = str(position[itterator]).split(', ')
                    if len(sort1) < 3:
                        del position[itterator]
                        del notearray[itterator]
                        continue
                    itterator += 1

                for i in range(0, len(notearray)):
                    print('Differenz Note/Zeit:\t\t' + notearray[i])
                    print('Zu Position, von Position:\t' + str(position[i]) + '\n')
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
    sys.stdout = normalstdout
    f.close()
    p.close()
    # LittleTranscriptor nehmen
    # https://www.youtube.com/watch?v=7K4hBdokhbE
    # nochmal mit 2ten monitor
    # jeder strich sind 2 sek keine 4
    # jede Hand neue Nummerierung
