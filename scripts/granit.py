import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
import glob
import os

def ensambleFR(spikeInstant, unitNumber, transientPeriod, simDuration):
    units = list(OrderedDict.fromkeys(unitNumber))
    
    if len(units) == 0:
        return 0
    else:
        meanFR = []
        for unit in units:
            MNSpikeInstants = [y for x, y in enumerate(spikeInstant) if unitNumber[x]==unit]
            numberOfSpikes = len([x for x in MNSpikeInstants if x>transientPeriod])
            meanFR.append(numberOfSpikes/(simDuration*1e-3 - transientPeriod*1e-3))

    #     popSlice = [y for x, y in enumerate(meanFR) if x>100 and x<200]
    #     sliceFR = sum(popSlice)/(len(popSlice))
    #     FR = sum(meanFR)/len(meanFR)

    #     plt.figure()
    #     plt.plot(units, meanFR, 'o')
    #     plt.axhline(y=FR, color='r', linestyle='-')
    #     plt.axhline(y=sliceFR, color='k', linestyle='-')
    #     plt.show()

        return sum(meanFR)/len(units)

###### Simulation settings and variables
duration = 4000
tmin = 1000
dt = 0.05
t = np.arange(0, duration, dt)
numberMN = 500
#pps = range(5, 575, 38)
pps = range(10, 80, 10)
figsFolder = '/home/pablo/git/master-thesis/figuras/'
trial = input("Trial number: ")
path = '/home/pablo/osf/Master-Thesis-Data/population/granit/trial' + trial

simTypes = ['c', 'c'] # Without and with RC

for simType in simTypes:
    files = glob.glob(path + '/*'+ simType + '.dat')
    spikesFiles = [x for x in files if 'spks' in x]
    spikesFiles.sort()
    forcesFiles = [x for x in files if 'force' in x]
    forcesFiles.sort()

    rateOnTrial = []
    forceOnTrial = []
    for filename in spikesFiles:
        spikeInstant = []
        unitNumber = []
        
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            spikeInstant.append(float(line.split()[0]))
            unitNumber.append(int(float(line.split()[1])))
        f.close()
        
        rateOnTrial.append(ensambleFR(spikeInstant, unitNumber,
            tmin, duration))
        print (rateOnTrial)

    plt.figure()
    plt.plot(pps, rateOnTrial)
    plt.show()

    for filename in forcesFiles:
        force = []
        instant = []
        
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            instant.append(float(line.split()[0]))
            force.append(float(line.split()[1]))
        f.close()
        
        staticForce = [y for x,y in enumerate(force) if instant[x]>tmin]
        forceOnTrial.append(np.mean(staticForce))
        #import pdb; pdb.set_trace()
        #plt.figure()
        #plt.plot(instant, force)
        #plt.show()

    plt.figure()
    plt.plot(pps, forceOnTrial)
    plt.show()
