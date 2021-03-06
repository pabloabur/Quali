import matplotlib
#matplotlib.use('TkAgg') # For X11 forwarding
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.fftpack import fft
import scipy.stats as stat

from ensembleRate import ensembleFR

def singleTrial(trial, subTrial):
    #****************************************
    #******* Simulation settings and variables
    #****************************************
    # Simulation
    duration = 9000
    tmin = 1000
    dt = 0.05
    simTypes = ['o', 's']
    fs=1/(dt*1e-3)

    # Biophysical parameters
    Esyn = 70
    numberMN = 300
    availableMNs = range(numberMN)
    recordedMN = 1#np.random.choice(availableMNs)
    #print('Recorded MN #{:}'.format(str(recordedMN)))

    # Files and paths
    dataPath = ('/home/pablo/osf/Master-Thesis-Data/population/psd/in/trial'
                + str(trial) + '/trial' + str(subtrial))

    plotF = {'d': [], 's': [], 'h': [], 'o': []}
    plotPSD = {'d': [], 's': [], 'h': [], 'o': []}
    plotFc = {'d': [], 's': [], 'h': [], 'o': []}
    plotCoherence = {'d': [], 's': [], 'h': [], 'o': []}
    sync = {'Forte': [], 'Normal': [], 'Fraco': [], 'Ausente': []}

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
        dendPotSOL = []
        instantaneousFiring = []

        #****************************************
        #******* Getting and processing spike data
        #****************************************
        fileName = dataPath + '/spike' + simType + '.dat'
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

        #if not any(MNSpikeInstants):
        #    print('No spikes for this MN')
        #elif len(MNSpikeInstants)==1:
        #    print('Only one spike for this MN')
        #else:
        #    for i in range(len(MNSpikeInstants)-1):
        #        instantaneousFiring.append(1000/(MNSpikeInstants[i+1]-
        #            MNSpikeInstants[i]))
        #    plt.figure()
        #    plt.plot(instantaneousFiring, '.')
        #    plt.ylabel('MN Instantaneous firing rate')
        #    plt.show()

        ### Plot spike times
        #plt.figure()
        #plt.plot(spikeTimes, spikeUnits, '.')
        #plt.title(simType)
        #plt.xlabel('Tempo (ms)')
        #plt.ylabel('Índices dos MNs')
        #plt.show()

        #****************************************
        #******* Getting and processing force data
        #****************************************
        fileName = dataPath + '/force' + simType + '.dat'
        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            for line in lines:
                taux.append(float(line.split()[0]))
                force.append(float(line.split()[1]))
            f.close()
        except:
            print('Warning: File ' + fileName + ' could not be opened.')

        staticForce = [y for x,y in enumerate(force) if taux[x]>tmin]
        var = np.var(staticForce)
        ave = np.mean(staticForce)

        ### Plot force
        #plt.figure()
        #plt.plot(taux, force)
        #plt.title(simType+', mean and variance after 1s: {:.4f} {:.6f}'.format(ave, var))
        #plt.xlabel('t (ms)')
        #plt.ylabel('Force (N)')
        #plt.grid()
        #plt.show()

        #     `boxcar`, `triang`, `blackman`, `hamming`, `hann`, `bartlett`,
        #         `flattop`, `parzen`, `bohman`, `blackmanharris`, `nuttall`,
        #         `barthann`, `kaiser` (needs beta), `gaussian` (needs standard
        #         deviation), `general_gaussian` (needs power, width), `slepian`
        #         (needs width), `dpss` (needs normalized half-bandwidth),
        #         `chebwin` (needs attenuation), `exponential` (needs decay scale),
        #         `tukey` (needs taper fraction)

        fr = 1
        nperseg = 4*fs/2/fr
        noverlap = 0#None
        nfft = None#8*nperseg
        #detrend = 'constant'
        detrend = False
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
            # RC effect
            dendPotSOL.append(float(line.split()[0]))
            EMG.append(float(line.split()[1]))
        f.close()

        # Membrane potentials from pools and EMG
        #plt.figure()
        #plt.plot(taux, dendPotSOL)
        #plt.title('SOL dendrite membrane potential '+simType)
        #plt.show()
        #import pdb; pdb.set_trace()
        #plt.figure()
        #plt.plot(taux, EMG)
        #plt.title('EMG '+simType)
        #plt.show()
        
        # TODO Decide on which nperseg
        nperseg = 5000
        staticEMG = [y for x,y in enumerate(EMG) if taux[x]>tmin]
        print(len(staticEMG))
        staticInput = [y for x,y in enumerate(dendPotSOL) if taux[x]>tmin]
        fc, coherence = signal.coherence(staticInput, staticEMG, fs, 'hann',
                                         nperseg, noverlap,
                                         nfft, detrend)

        ### Calculating confidence limit
        K = len(staticEMG)/(nperseg)
        alpha = .05
        F = stat.f.ppf(q=1-alpha, dfn=2, dfd=2*(K-1))
        print('Confidence Level: {:}'.format(str(F/(K-1+F))))

        ### Checking signals used for coherence
        #fi, inputPSD = signal.welch(staticEMG, fs, 'hann', nperseg, noverlap, nfft,
        #        detrend, scaling = scale)
        #plt.figure()
        #plt.xlabel('f (Hz)')
        #plt.ylabel('Power Spectrum Density EMG(mN^2)')
        #plt.xlim([0, 600])
        #plt.plot(fi, 1e6*inputPSD)
        #fi, inputPSD = signal.welch(staticInput, fs, 'hann', nperseg, noverlap, nfft,
        #        detrend, scaling = scale)
        #plt.figure()
        #plt.xlabel('f (Hz)')
        #plt.ylabel('Power Spectrum Density Gsyn(mN^2)')
        #plt.xlim([0, 600])
        #plt.plot(fi, 1e6*inputPSD)
        #plt.show()

        ### Plot used to see coherence at each trial
        #plt.figure()
        #plt.plot(fc, coherence)
        #plt.xlabel('f (Hz)')
        #plt.ylabel('Coherence')
        #plt.xlim([0, 50])
        #plt.grid()
        #plt.show()

        #****************************************
        #******* Gathering data for latter use
        #****************************************
        plotF[simType] = ff
        plotPSD[simType] = forcePSD
        plotFc[simType] = fc
        plotCoherence[simType] = coherence

    # This is just to check if they are the same. Seem to be. No reason 
    # to believe otherwise
    #print(plotF[0], plotF[1])
    #print(plotFc[0], plotFc[1])

    # Variables to be used in plots
    labels = {'d': 'Forte', 's': 'Normal', 'h': 'Fraco', 'o': 'Ausente'}
    symbols = {'d': 'k', 's': 'k--', 'h': 'k-.', 'o': 'k:'}

    # Plot PSD
    #plt.figure()
    #for simType in simTypes:
    #    plt.plot(plotF[simType], 1e6*plotPSD[simType], symbols[simType], label=labels[simType])
    #plt.xlabel('frequência (Hz)')
    #plt.ylabel('Densidade Espectral de Potência (mN$^2$)')
    #plt.grid()
    ##     plt.yscale('log')
    #plt.xlim([0, 50])
    #plt.ylim([0, 500])
    #plt.legend()
    #plt.show()

    # Plot coherence
    #plt.figure()
    #for simType in simTypes:
    #    plt.plot(plotFc[simType], plotCoherence[simType], symbols[simType], label=labels[simType])
    #plt.title('Cortico-EMG Coherence')
    #plt.xlabel('f (Hz)')
    #plt.ylabel('Coherence')
    #plt.xlim([0, 50])
    #plt.legend()
    #plt.show()

    return plotF, plotPSD, plotFc, plotCoherence

def allTrials(PSDs, f, Coherences, fc):
    # Files and paths
    filenamepsd = 'res_psdNew05'
    filenamecoh = 'res_cohNew05'
    figsFolder = '/home/pablo/git/master-thesis/figuras/'

    #****************************************
    #******* Calculating mean
    #****************************************
    simTypes = ['o', 's']
    symbols = {'d': 'k', 's': 'k--', 'h': 'k-.', 'o': 'k:'}
    meanPSD = {'d': [], 's': [], 'h': [], 'o': []}
    meanCoh = {'d': [], 's': [], 'h': [], 'o': []}
    labels = {'d': 'Forte', 's': 'Normal', 'h': 'Fraco', 'o': 'Ausente'}
    for simType in simTypes:
        meanPSD[simType] = np.mean([PSD[simType] for PSD in PSDs], axis=0)
        meanCoh[simType] = np.mean([coh[simType] for coh in Coherences], axis=0)

    #****************************************
    #******* Plotting
    #****************************************
    plt.figure()
    for simType in simTypes:
        # Here considering f was the same in all trials
        plt.plot(f[0]['o'], 1e6*meanPSD[simType], symbols[simType], label=labels[simType])
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Densidade espectral de potência (mN$^2$)')
    plt.grid()
    #plt.yscale('log')
    plt.xlim([0, 50])
    plt.ylim([0, 500])
    plt.legend()
    plt.show()
    #plt.savefig(figsFolder + filenamepsd + '.svg', format='svg')

    plt.figure()
    for simType in simTypes:
        # Here considering f was the same in all trials
        plt.plot(fc[0]['o'], meanCoh[simType], symbols[simType], label=labels[simType])
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Coerência córtico-muscular')
    plt.grid()
    #     plt.yscale('log')
    plt.xlim([0, 50])
    #     plt.xlim((0, 500))
    plt.legend()
    plt.show()
    #plt.savefig(figsFolder + filenamecoh + '.svg', format='svg')

# These are conveniently converted to a numpy 2d array latter because singleTrial function return numpy arrays
# TODO make it 10
numSubTrials = 5
psd = [[] for _ in range(1, numSubTrials+1)]
fpsd = [[] for _ in range(1, numSubTrials+1)]
coh = [[] for _ in range(1, numSubTrials+1)]
fc = [[] for _ in range(1, numSubTrials+1)]
reduc = [[] for _ in range(1, numSubTrials+1)]
syncs = [[] for _ in range(1, numSubTrials+1)]

trial = input('Trial number: ')
subtrials = [x for x in range(1, numSubTrials+1)]
for subtrial in subtrials:
    fpsd[subtrial-1], psd[subtrial-1], fc[subtrial-1], coh[subtrial-1] = singleTrial(trial, subtrial)

allTrials(psd, fpsd, coh, fc)
