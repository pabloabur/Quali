import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.optimize

figsFolder = '/home/pablo/git/master-thesis/figuras/'
trial = 4
path = '/home/pablo/osf/Master-Thesis-Data/population/dynamic/false_decay/trial'+ str(trial)
filenamedyn = 'dyn'
os.chdir(path)

simDuration_ms = 2000
stimPulseDuration = 0.2
timeStep_ms = 0.05
availableRCs = range(1, 601)
frequency1 = 5

recordedRCIndex = 382#np.random.choice(availableRCs)

# Preparing plot
plt.figure()
plt.title('Step change on RC '+str(recordedRCIndex))
plt.ylabel('RC firing rate (pps)')
plt.xlabel('Time (ms)')
plt.ylim([0, 400])

symbols = ['ko', 'k*', 'kX', 'k^']
freqs = [5, 15, 28, 45]
for i, freq in enumerate(freqs):
    firingRate = []
    unitNumber = []
    stimulus = []
    spikeInstant = []
    filename = 'output'+str(i+1)+'.dat'
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        spikeInstant.append(float(line.split()[0]))
        unitNumber.append(int(float(line.split()[1])))
    f.close()
    filename = 'stimulus'+str(i+1)+'.dat'
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        stimulus.append(float(line.split()[0]))
    f.close()
    
    #import pdb; pdb.set_trace()
    # Roughly determines bins, that start after each nonzero value
    nonZeroIdx = np.nonzero(stimulus)[0]
    # How long the stimulus lasts, in indexes
    # +1 is a correction because of the way it is implemented (check fortran plot)
    stimInterval_idx = int(stimPulseDuration/timeStep_ms)+1
    # bins, excluding the ones that do not finish (eventually, at the end of simulation)
    numberOfBins = int(len(nonZeroIdx)/stimInterval_idx)
    # Creates one array for each bin. This step already considers an integer length.
    bins = np.split(nonZeroIdx[:numberOfBins*stimInterval_idx], numberOfBins)
    # Adding the rightmost edge of the bin
    histBins = [x[0]*timeStep_ms for x in bins]
    histBins.append(simDuration_ms)

    RCSpikeInstants = [y for x, y in enumerate(spikeInstant) if unitNumber[x]==recordedRCIndex]
    spikesPerBin = np.histogram(RCSpikeInstants, bins=histBins)[0]
    binDuration1_ms = 1e3/float(frequency1)
    binDuration2_ms = 1e3/float(freq+5)
    # Since it is programmed to have only 3 stimulus on the first part of the simulation:
    firingRate = [y*1e3/binDuration1_ms if x<3 else y*1e3/binDuration2_ms for x,y in enumerate(spikesPerBin)]

    # Getting last spike instants of the RC in each bin
    abscissae = []
    accumulate=0
    for spikePerBin in spikesPerBin:
        accumulate+=spikePerBin
        abscissae.append(RCSpikeInstants[accumulate-1]) # -1 because arrays
                                                        # in python start at 0
        
        
    print(histBins)
    print(RCSpikeInstants)
    plt.plot(abscissae, firingRate, symbols[i], label=str(freq+5))
plt.legend()
plt.show()
