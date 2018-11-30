import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

# File settings
figsFolder = '/home/pablo/git/master-thesis/figuras/'
path = '/home/pablo/osf/Master-Thesis-Data/population/recruitment/false_decay/trial3'
filenameO = 'recruitO'
filenameC = 'recruitC'
filenameCxO = 'recruitCxO'
filenamezoom1 = 'recruitzoom1'
filenamezoom2 = 'recruitzoom2'
os.chdir(path)

spikeInstantMNo = []
unitNumberMNo = []
spikeInstantMNc = []
unitNumberMNc = []
#spikeInstantRC = []
#unitNumberRC = []

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

#filename = 'INc.dat'
#f = open(filename, 'r')
#lines = f.readlines()
#for line in lines:
#    spikeInstantRC.append(float(line.split()[0]))
#    unitNumberRC.append(int(float(line.split()[1])))
#f.close()

## Calculating firing rates
# Without RC
qntdInEachGroup = 3
availableS = [x for x in range(1, 76)]
availableFR = [x for x in range(76, 151)]
availableFF = [x for x in range(151, 301)]
SIndex = np.random.choice(availableS, qntdInEachGroup, replace=False)
FRIndex = np.random.choice(availableFR, qntdInEachGroup, replace=False)
FFIndex = np.random.choice(availableFF, qntdInEachGroup, replace=False)
Indexes = np.concatenate((SIndex, FRIndex, FFIndex), axis=None)
Indexes.sort(axis=0)

# Preparing plot
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

# With RC
ppsSc = []
ppsFRc = []
ppsFFc = []
Sc = [y for x, y in enumerate(spikeInstantMNc) if unitNumberMNc[x]==40]
FRc = [y for x, y in enumerate(spikeInstantMNc) if unitNumberMNc[x]==120]
FFc = [y for x, y in enumerate(spikeInstantMNc) if unitNumberMNc[x]==200]

for j in range(len(Sc)-1):
    ppsSc = np.append(ppsSc, [1000/(Sc[j+1]-Sc[j])])
del Sc[0]
for j in range(len(FRc)-1):
    ppsFRc = np.append(ppsFRc, [1000/(FRc[j+1]-FRc[j])])
del FRc[0]
for j in range(len(FFc)-1):
    ppsFFc = np.append(ppsFFc, [1000/(FFc[j+1]-FFc[j])])
del FFc[0]

plt.figure()
plt.title('Com célula de Renshaw')
plt.step(Sc, ppsSc, label='S')
plt.step(FRc, ppsFRc, label='FR')
plt.step(FFc, ppsFFc, label='FF')
plt.legend()
plt.xlabel('Tempo (ms)')
plt.ylabel('Taxa de disparo instantâneo (pps)')
#plt.show()

## Spike times
plt.figure()
# Maybe use plt.step
plt.title('Sem célula de Renshaw')
plt.plot(spikeInstantMNo, unitNumberMNo, 'k.')
plt.xlabel('Tempo (ms)')
plt.ylabel('Índice do motoneurônio')
plt.show()
#plt.savefig(figsFolder + filenameO + '.svg', format='svg')

plt.figure()
plt.title('Com célula de Renshaw')
plt.plot(spikeInstantMNc, unitNumberMNc, 'k.')
plt.xlabel('Tempo (ms)')
plt.ylabel('Índice do motoneurônio')
#plt.show()
#plt.savefig(figsFolder + filenameC + '.svg', format='svg')

plt.figure()
plt.plot(spikeInstantMNo, unitNumberMNo, 'k_', label='Sem célula de Renshaw')
plt.plot(spikeInstantMNc, unitNumberMNc, 'r|', label='Com célula de Renshaw')
plt.xlabel('Tempo (ms)')
plt.ylabel('Índice do motoneurônio')
plt.legend()
plt.show()
#plt.savefig(figsFolder + filenameCxO + '.svg', format='svg')

## spike times zoom
plt.figure()
plt.plot(spikeInstantMNc, unitNumberMNc, 'k.')
plt.xlabel('Tempo (ms)')
plt.ylabel('Índice do motoneurônio')
plt.xlim([830, 940])
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

#plt.figure()
#plt.plot(spikeInstantRC, unitNumberRC, '.')
#plt.xlabel('')
#plt.ylabel('')
#plt.show()
#plt.savefig(figsFolder + filenamenorm + '.svg', format='svg')
