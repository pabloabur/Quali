import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.fftpack import fft
import scipy.stats as stat

from ensembleRate import ensembleFR

#****************************************
#******* Simulation settings and variables
#****************************************
# Simulation
duration = 9000
tmin = 1000
dt = 0.05
t = np.arange(0, duration, dt)
simTypes = ['o', 'c'] # Without and with RC
fs=1/(dt*1e-3)

# Biophysical parameters
Esyn = 70
numberMN = 300
availableMNs = range(numberMN)
recordedMN = 1#np.random.choice(availableMNs)
print('Recorded MN #{:}'.format(str(recordedMN)))

# Files and paths
figsFolder = '/home/pablo/git/master-thesis/figuras/'
trial = input('Trial number: ')
dataPath = '/home/pablo/osf/Master-Thesis-Data/population/psd/natural/trial' + trial
filenamepsd = 'psd'

plotF = [[] for x in range(2)]
plotPSD = [[] for x in range(2)]
plotFc = [[] for x in range(2)]
plotCoherence = [[] for x in range(2)]

#****************************************
#******* Running simulation for each case
#****************************************
for j, simType in enumerate(simTypes):
    # Variables calculated
    force = []
    taux = []
    spikeTimes = []
    spikeUnits = []
    EMG = []
    inputConductance = []
    instantaneousFiring = []

    #****************************************
    #******* Getting and processing spike data
    #****************************************
    fileName = dataPath + '/spks' + simType + '.dat'
    f = open(fileName, 'r')
    lines = f.readlines()
    for line in lines:
        spikeTimes.append(float(line.split()[0]))
        spikeUnits.append(float(line.split()[1]))
    f.close()
    MNSpikeInstants = [y for x, y in enumerate(spikeTimes) if spikeUnits[x]==recordedMN]
    if not any(MNSpikeInstants):
        print('No spikes for this MN')
    elif len(MNSpikeInstants)==1:
        print('Only one spike for this MN')
    else:
        for i in range(len(MNSpikeInstants)-1):
            instantaneousFiring.append(1000/(MNSpikeInstants[i+1]-
                MNSpikeInstants[i]))
        #plt.figure()
        #plt.plot(instantaneousFiring, '.')
        #plt.ylabel('MN Instantaneous firing rate')
        #plt.show()
    plt.figure()
    plt.plot(spikeTimes, spikeUnits, '.')
    plt.xlabel('Tempo (ms)')
    plt.ylabel('Índices dos MNs')
    plt.show()

    #****************************************
    #******* Getting and processing force data
    #****************************************
    fileName = dataPath + '/force' + simType + '.dat'
    f = open(fileName, 'r')
    lines = f.readlines()
    for line in lines:
        taux.append(float(line.split()[0]))
        force.append(float(line.split()[1]))
    f.close()

    staticForce = [y for x,y in enumerate(force) if t[x]>tmin]
    var = np.var(staticForce)
    ave = np.mean(staticForce)
    plt.figure()
    plt.plot(t, force)
    plt.title('mean and variance after 1s: {:.4f} {:.6f}'.format(ave, var))
    plt.xlabel('t (ms)')
    plt.ylabel('Force (N)')
    plt.grid()
    plt.show()

    #     `boxcar`, `triang`, `blackman`, `hamming`, `hann`, `bartlett`,
    #         `flattop`, `parzen`, `bohman`, `blackmanharris`, `nuttall`,
    #         `barthann`, `kaiser` (needs beta), `gaussian` (needs standard
    #         deviation), `general_gaussian` (needs power, width), `slepian`
    #         (needs width), `dpss` (needs normalized half-bandwidth),
    #         `chebwin` (needs attenuation), `exponential` (needs decay scale),
    #         `tukey` (needs taper fraction)

    fr = 2
    nperseg = 4*fs/2/fr
    noverlap = 0#None
    nfft = None#8*nperseg
    detrend = 'constant'
    #detrend = False
    #detrend = 'linear'
    scale = 'spectrum'
    ff, forcePSD = signal.welch(staticForce, fs, 'hann', nperseg, noverlap,
            nfft, detrend, scaling = scale)

    #****************************************
    #******* Getting and processing for coherence
    #****************************************
    fileName = dataPath + '/g_emg' + simType + '.dat'
    f = open(fileName, 'r')
    lines = f.readlines()
    for line in lines:
        inputConductance.append(float(line.split()[0]))
        EMG.append(float(line.split()[1]))
    f.close()

    # Checking input
    #plt.figure()
    #plt.plot(t, inputConductance)
    #plt.title('conductance as I/V')
    #plt.show()
    
    print('Mean conductance, in module, is {:}'.format(str(abs(np.mean(
        inputConductance[int(tmin/0.05):])))))

    # Calculating confidence limit
    K = len(EMG)/(nperseg*2)
    alpha = .05
    F = stat.f.ppf(q=1-alpha, dfn=2, dfd=2*(K-1))
    print('Confidence Level: {:}'.format(str(F/(K-1+F))))

    fc, coherence = signal.coherence(inputConductance, np.abs(EMG), fs, ('tukey', 0.1), 10000, noverlap=5000)

    # Checking input PSD
    fi, inputPSD = signal.welch(inputConductance, fs, ('tukey', 0.1), nperseg, noverlap, nfft,
            detrend, scaling = scale)
    #plt.figure()
    #plt.title('Commom drive synaptic conductance PSD')
    #plt.xlabel('f (Hz)')
    #plt.ylabel('Power Spectrum Density(mN^2)')
    #plt.xlim([0, 60])
    #plt.plot(fi, 1e6*inputPSD)
    #plt.show()

    #****************************************
    #******* Gathering data for plot
    #****************************************
    plotF[j] = ff
    plotPSD[j] = forcePSD
    plotFc[j] = fc
    plotCoherence[j] = coherence

# This is just to check if they are the same. Seem to be. No reason 
# to believe otherwise
#print(plotF[0], plotF[1])
#print(plotFc[0], plotFc[1])

#****************************************
#******* Plotting
#****************************************
#import pdb; pdb.set_trace()
plt.figure()
plt.plot(plotF[0], 1e6*plotPSD[0], label='Sem CRs')
plt.plot(plotF[0], 1e6*plotPSD[1], label='Com CRs')
plt.xlabel('frequência (Hz)')
plt.ylabel('Densidade Espectral de Potência (mN$^2$)')
plt.grid()
#     plt.yscale('log')
plt.xlim([0, 50])
#     plt.xlim((0, 500))
plt.legend()
plt.show()
#plt.savefig(figsFolder + filenamepsd + '.svg', format='svg')

#plt.figure()
#plt.plot(plotFc[0], plotCoherence[0], label='Sem CRs')
#plt.plot(plotFc[0], plotCoherence[1], label='Com CRs')
#plt.title('Cortico-EMG Coherence')
#plt.xlabel('f (Hz)')
#plt.ylabel('Coherence')
#plt.xlim([0, 50])
#plt.legend()
#plt.show()
