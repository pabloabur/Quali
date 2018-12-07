import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

# File settings
figsFolder = '/home/pablo/git/master-thesis/figuras/'
path = '/home/pablo/osf/Master-Thesis-Data/population/onion/false_decay/trial1'
os.chdir(path)

inputFreqs = [90, 100, 110, 130, 140, 150, 170, 180, 190, 210]
qntdInEachGroup = 3
availableS = [x for x in range(1, 76)]
availableFR = [x for x in range(76, 151)]
availableFF = [x for x in range(151, 301)]

SIndex = np.random.choice(availableS, qntdInEachGroup, replace=False)
FRIndex = np.random.choice(availableFR, qntdInEachGroup, replace=False)
FFIndex = np.random.choice(availableFF, qntdInEachGroup, replace=False)
Indexes = np.concatenate((SIndex, FRIndex, FFIndex), axis=None)
Indexes.sort(axis=0)

# Without RC
# Preparing plot
for i, inputFreq in enumerate(inputFreqs):
    unitNumber = []
    spikeInstant = []
    filename = 'output'+str(i)+'.dat'
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        spikeInstant.append(float(line.split()[0]))
        unitNumber.append(int(float(line.split()[1])))

plt.figure()
plt.title('Sem célula de Renshaw')
plt.xlabel('Tempo (ms)')
plt.ylabel('Taxa de disparo instantâneo (pps)')

# Normalize data to be used by color map
norm = matplotlib.colors.Normalize(vmin=np.min(Indexes), vmax=np.max(Indexes))

# Choose color map
colorMap = matplotlib.cm.Greys

# create a ScalarMappable and initialize a data structure
mappable = matplotlib.cm.ScalarMappable(cmap=colorMap, norm=norm)
mappable.set_array([])

for index in Indexes:
    ppsO = []
    MNO = []
    MNO = [y for x, y in enumerate(spikeInstantMNo) if unitNumberMNo[x]==index]

    for j in range(len(MNO)-1):
        ppsO = np.append(ppsO, [1000/(MNO[j+1]-MNO[j])])
    del MNO[0]

    plt.step(MNO, ppsO, color=mappable.to_rgba(index))
plt.colorbar(mappable)
plt.show()

## With RC
## Preparing plot
#plt.figure()
#plt.title('Com célula de Renshaw')
#plt.xlabel('Tempo (ms)')
#plt.ylabel('Taxa de disparo instantâneo (pps)')
#
#for index in Indexes:
#    ppsC = []
#    MNC = []
#    MNC = [y for x, y in enumerate(spikeInstantMNc) if unitNumberMNc[x]==index]
#
#    for j in range(len(MNC)-1):
#        ppsC = np.append(ppsC, [1000/(MNC[j+1]-MNC[j])])
#    del MNC[0]
#
#    plt.step(MNC, ppsC, color=mappable.to_rgba(index))
#plt.colorbar(mappable)
#plt.show()
