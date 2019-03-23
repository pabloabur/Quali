import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

from ensembleRate import ensembleFR

###### Simulation settings and variables
duration = 4000
tmin = 1000
dt = 0.05
t = np.arange(0, duration, dt)
pps = [1] + list(range(75, 675, 75))
figsFolder = '/home/pablo/git/master-thesis/figuras/'
trial = input("Trial number: ")
path = '/home/pablo/osf/Master-Thesis-Data/population/granit/trial' + trial
filenamepps = 'granitrate'
filenameforce = 'granitforce'

simTypes = ['o', 'c'] # Without and with RC

rateOnTrialO = []
forceOnTrialO = []
rateOnTrialC = []
forceOnTrialC = []
for simType in simTypes:
    files = glob.glob(path + '/*'+ simType + '.dat')
    spikesFiles = [x for x in files if 'spks' in x]
    spikesFiles.sort()
    forcesFiles = [x for x in files if 'force' in x]
    forcesFiles.sort()

    for filename in spikesFiles:
        spikeInstant = []
        unitNumber = []
        
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            spikeInstant.append(float(line.split()[0]))
            unitNumber.append(int(float(line.split()[1])))
        f.close()
        
        if simType == 'o':
            rateOnTrialO.append(ensembleFR(spikeInstant, unitNumber,
                tmin, duration))
        elif simType == 'c':
            rateOnTrialC.append(ensembleFR(spikeInstant, unitNumber,
                tmin, duration))
        # Plots to understand results
        #plt.figure()
        #plt.plot(spikeInstant, unitNumber, '.')
        #plt.show()

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

        if simType == 'o':
            forceOnTrialO.append(np.mean(staticForce))
        elif simType == 'c':
            forceOnTrialC.append(np.mean(staticForce))
        # Plots to understand results
        #plt.figure()
        #plt.plot(instant, force)
        #plt.show()

plt.figure()
plt.plot(pps, rateOnTrialO, 'k', label='Sem CR')
plt.plot(pps, rateOnTrialC, 'k:', label='Com CR')
plt.plot(pps, np.array(rateOnTrialO) - np.array(rateOnTrialC), 'k--')
plt.legend()
plt.xlabel('Frequência de disparos das fibras descendentes (pps)')
plt.ylabel('Taxa de disparos da população de MNs (pps)')
plt.savefig(figsFolder + filenamepps + '.svg', format='svg')

plt.figure()
plt.plot(pps, forceOnTrialO, 'k', label='Sem CR')
plt.plot(pps, forceOnTrialC, 'k:', label='Com CR')
plt.plot(pps, np.array(forceOnTrialO) - np.array(forceOnTrialC), 'k--')
plt.legend()
plt.xlabel('Frequência de disparos das fibras descendentes (pps)')
plt.ylabel('Força (N)')
plt.savefig(figsFolder + filenameforce + '.svg', format='svg')
#plt.show()
