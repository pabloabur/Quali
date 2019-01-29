import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import signal
from scipy import integrate

###### File settings
duration = 9000
dt = 0.05
t = np.arange(0, duration, dt)
figsFolder = '/home/pablo/git/master-thesis/figuras/'
trial = input("Trial number: ")
path = '/home/pablo/osf/Master-Thesis-Data/population/onion/false_decay/trial' + trial
if trial=='5':
    filenameonionwithoutRC = 'onionwithoutRC'
    filenameonionwithRC = 'onionwithRC'
    filenamesonion = [filenameonionwithoutRC, filenameonionwithRC]
    filenameoniondvdt = 'oniondvdt'
elif trial=='6': # Increasing gamma, but I do not use it anymore on results
    filenameonionwithoutRC = 'onionwithoutRC2'
    filenameonionwithRC = 'onionwithRC2'
    filenamesonion = [filenameonionwithoutRC, filenameonionwithRC]
    filenameoniondvdt = 'oniondvdt2'
os.chdir(path)

###### Simulation settings and variables
# Available based on prevoius knowledge
available = [x for x in range(1, 100)]
qntd = 20
# 1 to 100 is a good range in the current simulation (check spikes plot below)
indexes = np.random.choice(available, qntd, replace=False)
#indexes.sort(axis=0)
dvdtMN = np.random.choice(indexes)
print('MNs chosen to plot: ' + str(indexes))
print('MN chosen to plot derivative: ' + str(dvdtMN))

dyo = np.zeros(len(t), np.float)
dyc = np.zeros(len(t), np.float)

simTypes = ['o', 'c'] # Without and with RC

# Window 400 ms wide as De Luca et al. (1982). 950 ms was used
# in De Luca and Erim (1994)
window = signal.windows.hann(int(400/dt))
windowArea = integrate.trapz(window, dx = dt)
normWindow = window/windowArea*1e3 # 1e3 multiplied because area was in mili
print('Area of normalized window: {:.1f}'.format(integrate.trapz(normWindow, dx = dt*1e-3)))

for filenameonion, simType in zip(filenamesonion, simTypes):
    # For spike times
    unitNumber = []
    spikeInstant = []
    filename = 'output' + simType + '.dat'
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        spikeInstant.append(float(line.split()[0]))
        unitNumber.append(int(float(line.split()[1])))

    #plt.figure()
    #plt.plot(spikeInstant,unitNumber)
    #plt.show()

    # Normalize data to be used by color map
    norm = matplotlib.colors.Normalize(vmin=np.min(indexes), vmax=np.max(indexes))

    # Choose color map
    colorMap = matplotlib.cm.tab20

    # create a ScalarMappable and initialize a data structure
    mappable = matplotlib.cm.ScalarMappable(cmap=colorMap, norm=norm)
    mappable.set_array([])

    # Preparing plot
    plt.figure()
    plt.xlabel('Tempo (ms)')
    plt.ylabel('Taxa de disparo (pps)')

    # For muscle force
    filename = 'force' + simType + '.dat'
    f = open(filename, 'r')
    lines = f.readlines()
    tForce = []
    force = []
    for line in lines:
        tForce.append(int(float(line.split()[0])))
        force.append(int(float(line.split()[1])))

    ###### Simulation
    for index in indexes:
        FR = np.array([])
        spkTrain = np.zeros(len(t))

        # Calculate instantaneous firing rate
        MNspikes = [y for x, y in enumerate(spikeInstant) if unitNumber[x]==index]
        for instant in MNspikes:
            spkTrain[int(instant/dt)] = 1
        FR = signal.convolve(spkTrain, normWindow, mode = 'same')

        # Getting values for the other plot (happens only once)
        if index==dvdtMN:
            if simType=='o':
                dyo[0:-1] = np.diff(FR)/np.diff(t)
                dyo[-1] = (FR[-1] - FR[-2])/(t[-1] - t[-2])
            if simType=='c':
                dyc[0:-1] = np.diff(FR)/np.diff(t)
                dyc[-1] = (FR[-1] - FR[-2])/(t[-1] - t[-2])
    
        # Identifying where FR starts and ends
        if MNspikes:
            firstSpike = min(MNspikes)
            lastSpike = max(MNspikes)
            selectedFR = [float('nan') if y<firstSpike or y>lastSpike else FR[x] for x, y in enumerate(t)]
        else:
            selectedFR = [float('nan') for x in FR]
        #import pdb; pdb.set_trace()
        plt.plot(t, selectedFR, linewidth=2, color=mappable.to_rgba(index))
        #plt.plot(tForce, force, 'k--') # To plot force on graph
    plt.colorbar(mappable)
    plt.savefig(figsFolder + filenameonion + '.svg', format='svg')

#plt.figure()
#plt.plot(t, dyo*1e3,
#         label='Motoneurônio {} sem célula de Renshaw'.format(dvdtMN))
#plt.plot(t, dyc*1e3,
#         label='Motoneurônio {} com célula de Renshaw'.format(dvdtMN))
#plt.legend()
#plt.xlabel('Taxa de disparo das fibras descendentes (pps)')
#plt.ylabel('Derivada da taxa de disparo')
#plt.show()
plt.savefig(figsFolder + filenameoniondvdt + '.svg', format='svg')
