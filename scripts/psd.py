import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.fftpack import fft
import scipy.stats as stat

from ensembleRate import ensembleFR

def singleTrial(trial, subTrial, simMVC):
    #****************************************
    #******* Simulation settings and variables
    #****************************************
    # Simulation
    # TODO uncomment those values
    duration = 1500#9000
    tmin = 200#1000
    dt = 0.05
    # TODO this is only for noise strategy
    simTypes = ['o', 's']#['o', 'h', 's', 'd'] # Without and with RC
    fs=1/(dt*1e-3)

    # Biophysical parameters
    Esyn = 70
    numberMN = 300
    availableMNs = range(numberMN)
    recordedMN = 1#np.random.choice(availableMNs)
    #print('Recorded MN #{:}'.format(str(recordedMN)))

    # Files and paths
    dataPath = ('/home/pablo/osf/Master-Thesis-Data/population/psd/natural/trial'
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
        inputConductance = []
        instantaneousFiring = []

        #****************************************
        #******* Getting and processing spike data
        #****************************************
        fileName = dataPath + '/spike' + simMVC + simType + '.dat'
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

        # Plot used for more detailed investigation
        plt.figure()
        plt.plot(spikeTimes, spikeUnits, '.')
        plt.title(simType)
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Índices dos MNs')
        plt.show()

        #****************************************
        #******* Getting and processing force data
        #****************************************
        fileName = dataPath + '/force' + simMVC + simType + '.dat'
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

        # TODO comment this
        # Plot used for more detailed investigation
        plt.figure()
        plt.plot(taux, force)
        plt.title(simType+', mean and variance after 1s: {:.4f} {:.6f}'.format(ave, var))
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
        #******* Getting and processing for coherence# Most of this is not used anymore
        #****************************************
        fileName = dataPath + '/g_emg' + simMVC + simType + '.dat'
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
        
        #print('Mean conductance, in module, is {:}'.format(str(abs(np.mean(
        #   inputConductance[int(tmin/0.05):])))))

        # Calculating confidence limit
        K = len(EMG)/(nperseg*2)
        alpha = .05
        F = stat.f.ppf(q=1-alpha, dfn=2, dfd=2*(K-1))
        print('Confidence Level: {:}'.format(str(F/(K-1+F))))

        fc, coherence = signal.coherence(inputConductance, np.abs(EMG), fs, ('tukey', 0.1), 10000, noverlap=5000)

        # Checking input PSD
        #fi, inputPSD = signal.welch(inputConductance, fs, ('tukey', 0.1), nperseg, noverlap, nfft,
        #        detrend, scaling = scale)
        #plt.figure()
        #plt.title('Commom drive synaptic conductance PSD')
        #plt.xlabel('f (Hz)')
        #plt.ylabel('Power Spectrum Density(mN^2)')
        #plt.xlim([0, 60])
        #plt.plot(fi, 1e6*inputPSD)
        #plt.show()
        # TODO comment this
        # Plot used for more detailed investigation
        plt.figure()
        plt.plot(fc, coherence)
        plt.xlabel('f (Hz)')
        plt.ylabel('Coherence')
        plt.xlim([0, 50])
        plt.grid()
        plt.show()

        #****************************************
        #******* Getting synchronization coefficients
        #****************************************
        fileName = dataPath + '/sync' + simMVC + simType + '.dat'
        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            for line in lines:
                sync[simType] = float(line.split()[0])
            f.close()
        except:
            print('Warning: File ' + fileName + ' could not be opened.')

        #****************************************
        #******* Gathering data for latter use
        #****************************************
        plotF[simType] = ff
        plotPSD[simType] = forcePSD
        #plotFc[j] = fc
        #plotCoherence[j] = coherence

    # This is just to check if they are the same. Seem to be. No reason 
    # to believe otherwise
    #print(plotF[0], plotF[1])
    #print(plotFc[0], plotFc[1])

    #****************************************
    #******* Calculating reduction in peaks
    #****************************************
    # TODO I think I will not make this calculation anymore, only in noise strategy
    #peaksO, _ = signal.find_peaks(plotPSD['o'])
    #peaksC, _ = signal.find_peaks(plotPSD['s'])
    #peaksO = [x for x in peaksO if abs(10-x)<1 or abs(20-x)<1 or abs(30-x)<1 or abs(40-x)<1]
    #peaksC = [x for x in peaksC if abs(10-x)<1 or abs(20-x)<1 or abs(30-x)<1 or abs(40-x)<1]
    ## TODO uncomment this but be ware that previosly the peaks vector had length of only 1, 
    ## which caused an error
    #reducPerc = 0#plotPSD['o'][peaksO]/plotPSD['s'][peaksC]

    # Plot PSD
    plt.figure()
    labels = {'d': 'Forte', 's': 'Normal', 'h': 'Fraco', 'o': 'Ausente'}
    symbols = {'d': 'k', 's': 'k--', 'h': 'k-.', 'o': 'k:'}
    for simType in simTypes:
        #import pdb; pdb.set_trace()
        plt.plot(plotF[simType], 1e6*plotPSD[simType], symbols[simType], label=labels[simType])
    # TODO uncomment
    #plt.plot(peaksC, 1e6*plotPSD['s'][peaksC], 'rx')
    #plt.plot(peaksO, 1e6*plotPSD['o'][peaksO], 'gx')
    plt.xlabel('frequência (Hz)')
    plt.ylabel('Densidade Espectral de Potência (mN$^2$)')
    plt.grid()
    #     plt.yscale('log')
    plt.xlim([0, 50])
    #     plt.xlim((0, 500))
    plt.legend()
    plt.show()

    # Plot coherence
    #plt.figure()
    #plt.plot(plotFc[0], plotCoherence[0], label='Sem CRs')
    #plt.plot(plotFc[0], plotCoherence[1], label='Com CRs')
    #plt.title('Cortico-EMG Coherence')
    #plt.xlabel('f (Hz)')
    #plt.ylabel('Coherence')
    #plt.xlim([0, 50])
    #plt.legend()
    #plt.show()

    return plotF, plotPSD, sync

def allTrials(PSDs, f, red):
    # Files and paths
    filenamepsd = 'res_psd'
    figsFolder = '/home/pablo/git/master-thesis/figuras/'

    #****************************************
    #******* Calculating mean
    #****************************************
    simTypes = ['o', 'h', 's', 'd'] # Without and with RC
    meanPSD = {'d': [], 's': [], 'h': [], 'o': []}
    for simType in simTypes:
        meanPSD[simType] = np.mean([PSD[simType] for PSD in PSDs], axis=0)

    #****************************************
    #******* Plotting
    #****************************************
    plt.figure()
    plt.plot(f, 1e6*psdo, label='Sem CRs')
    plt.plot(f, 1e6*psdc, label='Com CRs')
    plt.xlabel('frequência (Hz)')
    plt.ylabel('Densidade Espectral de Potência (mN$^2$)')
    plt.grid()
    #     plt.yscale('log')
    plt.xlim([0, 50])
    #     plt.xlim((0, 500))
    plt.legend()
    # TODO configure for saving only again
    plt.show()
    #plt.savefig(figsFolder + filenamepsd + '.svg', format='svg')

    print('Reduction of peaks in 10, 20, 30 and 40 Hz, respectively, in percentage:')
    print(1-red)

# These are conveniently converted to a numpy 2d array latter because singleTrial function return numpy arrays
numSubTrials = 10
psd = [[] for _ in range(1, numSubTrials+1)]
f = [[] for _ in range(1, numSubTrials+1)]
reduc = [[] for _ in range(1, numSubTrials+1)]
syncs = [[] for _ in range(1, numSubTrials+1)]

trial = input('Trial number: ')
mvc = input('MVC percentage: ')
subtrials = [x for x in range(1, numSubTrials+1)]
#subtrial = input('Subtrial number: ')
for subtrial in subtrials:
    f[subtrial-1], psd[subtrial-1], syncs[subtrial-1] = singleTrial(trial, subtrial, str(mvc))

allTrials(psd, f, syncs)
