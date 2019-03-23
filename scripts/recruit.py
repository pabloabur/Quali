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
filenameCfirst = 'recruitFirstsC'
filenameOfirst = 'recruitFirstsO'

trials = ['3', '4']

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
    if trial=='3': 
        plt.figure()
        plt.plot(spikeInstantMNo, unitNumberMNo, 'k.', label='Sem célula de Renshaw')
        plt.plot(spikeInstantMNc, unitNumberMNc, 'r.', label='Com célula de Renshaw')
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.legend()
        plt.savefig(figsFolder + filenameCxO + '.svg', format='svg')

        ## spike times zoom
        plt.figure()
        plt.plot(spikeInstantMNc, unitNumberMNc, 'k.')
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.xlim([860, 980])
        plt.ylim([200, 240])
        plt.savefig(figsFolder + filenamezoom1 + '.svg', format='svg')

        plt.figure()
        plt.plot(spikeInstantMNc, unitNumberMNc, 'k.')
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.xlim([140, 250])
        plt.ylim([0, 40])
        plt.savefig(figsFolder + filenamezoom2 + '.svg', format='svg')

    elif trial == '4':
        fig, ax = plt.subplots(1)
        plt.plot(spikeInstantMNo, unitNumberMNo, 'k.')
        ax.plot((spikeInstantMNo, spikeInstantMNo), (77, 104), 'k-', linewidth=0.1)
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.xlim([120, 260])
        plt.ylim([77, 104])
        plt.savefig(figsFolder + filenamepoissonO + '.svg', format='svg')

        fig, ax = plt.subplots(1)
        plt.plot(spikeInstantMNc, unitNumberMNc, 'k.')
        ax.plot((spikeInstantMNc, spikeInstantMNc), (77, 104), 'k-', linewidth=0.1)
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.xlim([160, 310])
        plt.ylim([77, 104])
        plt.savefig(figsFolder + filenamepoissonC + '.svg', format='svg')

        plt.figure()
        plt.plot(spikeInstantMNc, unitNumberMNc, 'k.')
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.xlim([140, 230])
        plt.ylim([50, 85])
        plt.axhline(75.5, color='k', linestyle=':')
        referenceInstant = [y for x, y in enumerate(spikeInstantMNc) if
                    unitNumberMNc[x]==83][0]
        plt.vlines(x=referenceInstant, ymin=47, ymax=83, color='k', linestyle='--')
        analysedInstant = [y for x, y in enumerate(spikeInstantMNc) if
                    unitNumberMNc[x]==53][0]
        plt.hlines(y=53, xmin=referenceInstant, xmax=analysedInstant, color='k')
        analysedInstant = [y for x, y in enumerate(spikeInstantMNc) if
                    unitNumberMNc[x]==66][0]
        plt.hlines(y=66, xmin=referenceInstant, xmax=analysedInstant, color='k')
        analysedInstant = [y for x, y in enumerate(spikeInstantMNc) if
                    unitNumberMNc[x]==72][0]
        plt.hlines(y=72, xmin=referenceInstant, xmax=analysedInstant, color='k')
        plt.savefig(figsFolder + filenamerecruit + '.svg', format='svg')

    #plt.savefig(figsFolder + filenameCxO + '.svg', format='svg')
    #plt.figure()
    #plt.plot(spikeInstantRC, unitNumberRC, '.')
    #plt.xlabel('')
    #plt.ylabel('')
    #plt.show()
    #plt.savefig(figsFolder + filenamenorm + '.svg', format='svg')

# Second part of the plots (done here for convenience)
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

    found = []
    times = []
    for j, i in enumerate(unitNumberMNo):
        if i not in found:
            found.append(i)
            times.append(spikeInstantMNo[j])
    if trial=='3':
        current = []
        current = times
    else:
        plt.figure()
        plt.plot(times, found, 'k.')
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.savefig(figsFolder + filenameOfirst + '.svg', format='svg')
    found = []
    times = []
    for j, i in enumerate(unitNumberMNc):
        if i not in found:
            found.append(i)
            times.append(spikeInstantMNc[j])
    if trial=='3':
        current = []
        current = times
    else:
        #import pdb; pdb.set_trace()
        plt.figure()
        plt.plot(times, found, 'k.')
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índice do motoneurônio')
        plt.savefig(figsFolder + filenameCfirst + '.svg', format='svg')
#plt.show()
