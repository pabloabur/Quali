import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as ptchs
import numpy as np
import os

# File settings
figsFolder = '/home/pablo/git/master-thesis/figuras/'
filenameCxO = 'recruitCxO'
filenamezoom1 = 'recruitzoom1'
filenamezoom2 = 'recruitzoom2'
filenamepoissonO = 'recruitpoissonO'
filenamepoissonC = 'recruitpoissonC'
filenamerecruit = 'revrecruit'

trials = ['1', '2']#, '3'] # current, poisson and varying gamma trials, respectively

for trial in trials:
    # Initializing variables
    spikeInstantMNo = []
    unitNumberMNo = []
    spikeInstantMNc = []
    unitNumberMNc = []
    t = []
    force = []
    #spikeInstantRC = []
    #unitNumberRC = []

    # Make simulations using trial with injected current
    path = '/home/pablo/osf/Master-Thesis-Data/population/recruitment/false_decay/trial'+trial
    os.chdir(path)

    filename = 'MNo.dat'
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        spikeInstantMNo.append(float(line.split()[0]))
        unitNumberMNo.append(int(float(line.split()[1])))
    f.close()

    filename = 'MNc.dat'
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        spikeInstantMNc.append(float(line.split()[0]))
        unitNumberMNc.append(int(float(line.split()[1])))
    f.close()

    filename = 'forcec.dat'
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        t.append(float(line.split()[0]))
        force.append(int(float(line.split()[1])))
    f.close()

    #plt.figure()
    #plt.plot(t, force)
    #plt.show()

    #filename = 'INc.dat'
    #f = open(filename, 'r')
    #lines = f.readlines()
    #for line in lines:
    #    spikeInstantRC.append(float(line.split()[0]))
    #    unitNumberRC.append(int(float(line.split()[1])))
    #f.close()

    # Plots depending on trial
    if trial=='1': 
        plt.figure()
        plt.plot(spikeInstantMNo, unitNumberMNo, 'k.', label='Sem célula de Renshaw')
        plt.plot(spikeInstantMNc, unitNumberMNc, 'r.', label='Com célula de Renshaw')
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.legend()
        #plt.show()
        plt.savefig(figsFolder + filenameCxO + '.svg', format='svg')

        ## spike times zoom
        plt.figure()
        plt.plot(spikeInstantMNc, unitNumberMNc, 'k.')
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.xlim([860, 980])
        plt.ylim([200, 240])
        #plt.show()
        plt.savefig(figsFolder + filenamezoom1 + '.svg', format='svg')

        plt.figure()
        plt.plot(spikeInstantMNc, unitNumberMNc, 'k.')
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.xlim([140, 250])
        plt.ylim([0, 40])
        #plt.show()
        plt.savefig(figsFolder + filenamezoom2 + '.svg', format='svg')

    elif trial == '2':
        # Create rectangles area
        recto1 = ptchs.Rectangle((160.0,83.5), 5.0, 4.0, fill=False, edgecolor='k')
        rectc1 = ptchs.Rectangle((259.5,77.5), 5.0, 5.2, fill=False, edgecolor='k')
        rectc2 = ptchs.Rectangle((261.5,93), 4.0, 4.0, fill=False, edgecolor='k')
        rectc3 = ptchs.Rectangle((217.5,82.5), 3, 3, fill=False, edgecolor='k')

        fig, ax = plt.subplots(1)
        plt.plot(spikeInstantMNo, unitNumberMNo, 'k.')
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.xlim([120, 260])
        plt.ylim([77, 104])
        ax.add_patch(recto1)
        plt.savefig(figsFolder + filenamepoissonO + '.svg', format='svg')

        fig, ax = plt.subplots(1)
        plt.plot(spikeInstantMNc, unitNumberMNc, 'k.')
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.xlim([140, 280])
        plt.ylim([77, 104])
        ax.add_patch(rectc1)
        ax.add_patch(rectc2)
        ax.add_patch(rectc3)
        plt.savefig(figsFolder + filenamepoissonC + '.svg', format='svg')

        plt.figure()
        plt.plot(spikeInstantMNc, unitNumberMNc, 'k.')
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.xlim([140, 230])
        plt.ylim([47, 79])
        plt.axhline(75.5, color='k', linestyle=':')
        referenceInstant = [y for x, y in enumerate(spikeInstantMNc) if
                    unitNumberMNc[x]==78][0]
        plt.vlines(x=referenceInstant, ymin=47, ymax=78, color='k', linestyle='--')
        analysedInstant = [y for x, y in enumerate(spikeInstantMNc) if
                    unitNumberMNc[x]==54][0]
        plt.hlines(y=54, xmin=referenceInstant, xmax=analysedInstant, color='k')
        analysedInstant = [y for x, y in enumerate(spikeInstantMNc) if
                    unitNumberMNc[x]==66][0]
        plt.hlines(y=66, xmin=referenceInstant, xmax=analysedInstant, color='k')
        analysedInstant = [y for x, y in enumerate(spikeInstantMNc) if
                    unitNumberMNc[x]==71][0]
        plt.hlines(y=71, xmin=referenceInstant, xmax=analysedInstant, color='k')
        #plt.show()
        plt.savefig(figsFolder + filenamerecruit + '.svg', format='svg')

    #plt.savefig(figsFolder + filenameCxO + '.svg', format='svg')
    #plt.figure()
    #plt.plot(spikeInstantRC, unitNumberRC, '.')
    #plt.xlabel('')
    #plt.ylabel('')
    #plt.show()
    #plt.savefig(figsFolder + filenamenorm + '.svg', format='svg')
