import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt
import random

if __name__ == '__main__':
    try:
        os.mkdir('ExamplesYOLO')
    except OSError:
        print("Folder ExampleYOLO already exists.\n Proceed to creating examples.")
    os.chdir(os.getcwd()+'/ExamplesYOLO')
    song = []
    done = False
    for i in range(1, 501):
        p = open('Example' + str(i) + '.txt', 'w')
        for j in range(0, 200):
            if random.random() <= 0.025 and j > 60:
                done = True
                patternlength = random.randint(10,60)
                patternposition = random.randint (0, j-61)
                for k in range(0, patternlength):
                    song.append(song[patternposition + k])
                    p.write(str(j+k) + ',' + str(song[patternposition + k]) + ',1\n')
            else:
                note = random.randint(0, 128)
                p.write(str(j) + ',' + str(note) + ',1\n')
                song.append(note)
            if done:
                done = False
                j = j + patternlength
                if j >= 200:
                    break
        p.close()
    for i in range(1, 501):
        p = open('Example' + str(i) + '.txt', 'r')
        time = []
        note = []
        while True:
            nextline = p.readline()
            if nextline == '':
                break
            else:
                informations = nextline.split(',')
                time.append(int(informations[0]))
                note.append(int(informations[1]))
        plt.yticks(np.arange(0,128,10))
        plt.xticks(np.arange(0,300,40))
        plt.scatter(time, note)
        plt.xlabel('Note in Track')
        plt.ylabel('Notepitch')
        plt.savefig('Example'+str(i)+'.png', dpi=200)
        plt.clf()
        p.close()


