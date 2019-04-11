import matplotlib
import matplotlib.pyplot as plt
import numpy as np

###### File settings
dataPath = '/home/pablo/osf/Master-Thesis-Data/population/farina/trial1/trial1/'
duration = 500
dt = 0.05
t = np.arange(0, duration, dt)
simTypes = ['o', 's']

#****************************************
#******* Running simulation for each case
#****************************************
for i, simType in enumerate(simTypes):
    #****************************************
    #******* Getting and processing spike data
    #****************************************
    fileName = dataPath + '/spike' + simType + '.dat'
    spikeTimes = []
    spikeUnits = []
    try:
        f = open(fileName, 'r')
    except:
        print('Warning: File ' + fileName + ' could not be opened.')
        continue
    lines = f.readlines()
    for line in lines:
        spikeTimes.append(float(line.split()[0]))
        spikeUnits.append(float(line.split()[1]))
    f.close()
    #MNSpikeInstants = [y for x, y in enumerate(spikeTimes) if spikeUnits[x]==recordedMN]

    # Plot used for more detailed investigation
    plt.figure()
    plt.plot(spikeTimes, spikeUnits, '.')
    plt.title(simType)
    plt.xlabel('Tempo (ms)')
    plt.ylabel('Índices dos MNs')
    plt.show()
