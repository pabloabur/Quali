import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.interpolate import UnivariateSpline

###### File settings
figsFolder = '/home/pablo/git/master-thesis/figuras/'
trial = 2
path = '/home/pablo/osf/Master-Thesis-Data/population/onion/false_decay/trial'+ str(trial)
if trial==1:
    filenameonionwithoutRC = 'onionwithoutRC'
    filenameonionwithRC = 'onionwithRC'
    filenamesonion = [filenameonionwithoutRC, filenameonionwithRC]
    filenameoniondvdt = 'oniondvdt'
elif trial==2:
    filenameonionwithoutRC = 'onionwithoutRC2'
    filenameonionwithRC = 'onionwithRC2'
    filenamesonion = [filenameonionwithoutRC, filenameonionwithRC]
    filenameoniondvdt = 'oniondvdt2'
os.chdir(path)

###### Simulation settings and variables
inputFreqs = [150, 300, 450, 600, 750, 900, 1050, 1200, 1350, 1500]
qntdInEachGroup = 3
availableS = [x for x in range(1, 76)]
availableFR = [x for x in range(76, 151)]
availableFF = [x for x in range(151, 301)]

SIndex = np.random.choice(availableS, qntdInEachGroup, replace=False)
FRIndex = np.random.choice(availableFR, qntdInEachGroup, replace=False)
FFIndex = np.random.choice(availableFF, qntdInEachGroup, replace=False)
indexes = np.concatenate((SIndex, FRIndex, FFIndex), axis=None)
indexes.sort(axis=0)
dvdtMN = np.random.choice(indexes)
print(indexes)
print(dvdtMN)

meanFR = np.zeros(len(inputFreqs))
dyo = np.zeros(len(inputFreqs), np.float)
dyc = np.zeros(len(inputFreqs), np.float)

# Normalize data to be used by color map
norm = matplotlib.colors.Normalize(vmin=np.min(indexes), vmax=np.max(indexes))

# Choose color map
colorMap = matplotlib.cm.tab20

# create a ScalarMappable and initialize a data structure
mappable = matplotlib.cm.ScalarMappable(cmap=colorMap, norm=norm)
mappable.set_array([])

simTypes = ['o', 'c'] # Without and with RC

for filenameonion, simType in zip(filenamesonion, simTypes):
    # Preparing plot
    plt.figure()
    plt.xlabel('Taxa de disparo do comando descendente (pps)')
    plt.ylabel('Taxa de disparo média do motoneurônio (pps)')

    ###### Simulation
    for index in indexes:
        for i, inputFreq in enumerate(inputFreqs):
            FR = np.array([])
            unitNumber = []
            spikeInstant = []
            filename = 'output' + str(i) + simType + '.dat'
            f = open(filename, 'r')
            lines = f.readlines()
            for line in lines:
                spikeInstant.append(float(line.split()[0]))
                unitNumber.append(int(float(line.split()[1])))

            MN = [y for x, y in enumerate(spikeInstant) if unitNumber[x]==index]
            steadyMN = [x for x in MN if x>1000]

            # Calculate instantaneous firing rate
            for k in range(len(steadyMN)-1):
                FR = np.append(FR, [1000 / (steadyMN[k+1] - steadyMN[k])])
            # Calculate the mean
            if not FR.size:
                meanFR[i] = 0
            else:
                meanFR[i] = np.mean(FR)

            # Getting values for next plot
            if index==dvdtMN:
                if simType=='o':
                    dyo[0:-1] = np.diff(meanFR)/np.diff(inputFreqs)
                    dyo[-1] = (meanFR[-1] - meanFR[-2])/(inputFreqs[-1] - inputFreqs[-2])
                if simType=='c':
                    dyc[0:-1] = np.diff(meanFR)/np.diff(inputFreqs)
                    dyc[-1] = (meanFR[-1] - meanFR[-2])/(inputFreqs[-1] - inputFreqs[-2])
    
        #import pdb; pdb.set_trace()
        plt.plot(inputFreqs, meanFR, linewidth=2, color=mappable.to_rgba(index))
    plt.colorbar(mappable)
    plt.savefig(figsFolder + filenameonion + '.svg', format='svg')

plt.figure()
plt.plot(inputFreqs, dyo,
         label='Motoneurônio {} sem célula de Renshaw'.format(dvdtMN))
plt.plot(inputFreqs, dyc,
         label='Motoneurônio {} com célula de Renshaw'.format(dvdtMN))
plt.legend()
plt.xlabel('Taxa de disparo das fibras descendentes (pps)')
plt.ylabel('Derivada da taxa de disparo')
#plt.show()
plt.savefig(figsFolder + filenameoniondvdt + '.svg', format='svg')
