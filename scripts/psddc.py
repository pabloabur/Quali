import matplotlib
#matplotlib.use('TkAgg') # For X11 forwarding
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
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
    duration = 11000
    tmin = 1000
    dt = 0.05
    simTypes = ['d', 's', 'h', 'o']
    fs=1/(dt*1e-3)

    # Biophysical parameters
    Esyn = 70
    numberMN = 300
    availableMNs = range(numberMN)
    recordedMN = 1#np.random.choice(availableMNs)
    #print('Recorded MN #{:}'.format(str(recordedMN)))

    # Files and paths
    dataPath = ('/home/pablo/osf/Master-Thesis-Data/population/psd/dc/trial'
                + str(trial) + '/trial' + str(subtrial))

    plotF = {'d': [], 's': [], 'h': [], 'o': []}
    plotPSD = {'d': [], 's': [], 'h': [], 'o': []}
    plotFc = {'d': [], 's': [], 'h': [], 'o': []}
    plotCoherence = {'d': [], 's': [], 'h': [], 'o': []}

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
        #plt.figure()
        #plt.plot(spikeTimes, spikeUnits, '.')
        #plt.title(simType)
        #plt.xlabel('Tempo (ms)')
        #plt.ylabel('Índices dos MNs')
        #plt.show()

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

        # Plot used for more detailed investigation
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
        noverlap = None
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
        fileName = dataPath + '/g_emg' + simMVC + simType + '.dat'
        f = open(fileName, 'r')
        lines = f.readlines()
        for line in lines:
            dendPotSOL.append(float(line.split()[0]))
            EMG.append(float(line.split()[1]))
        f.close()

        # Membrane potentials from pools and EMG
        #plt.figure()
        #plt.plot(taux, dendPotSOL)
        #plt.title('SOL dendrite membrane potential '+simType)
        #plt.show()
        #plt.figure()
        #plt.plot(taux, EMG)
        #plt.title('EMG '+simType)
        #plt.show()
        
        #print('Mean conductance, in module, is {:}'.format(str(abs(np.mean(
        #   inputConductance[int(tmin/0.05):])))))

        # Using parameter below I can see decrease in coherence peak
        nperseg = 6000
        staticEMG = [y for x,y in enumerate(EMG) if taux[x]>tmin]
        staticInput = [y for x,y in enumerate(dendPotSOL) if taux[x]>tmin]
        fc, coherence = signal.coherence(staticInput, staticEMG, fs, 'hann',
                                         nperseg, noverlap,
                                         nfft, detrend)

        # Calculating confidence limit
        K = len(staticEMG)/(nperseg)
        alpha = .05
        F = stat.f.ppf(q=1-alpha, dfn=2, dfd=2*(K-1))
        print('Confidence Level: {:}'.format(str(F/(K-1+F))))

        # Checking input PSD
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
    #labels = {'d': 'Forte', 's': 'Normal', 'h': 'Fraco', 'o': 'Ausente'}
    #symbols = {'d': 'k', 's': 'k--', 'h': 'k-.', 'o': 'k:'}
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

def allTrials(PSDs, f, Coherences, fc, mvc):
    # Files and paths
    if mvc=='70':
        filenamepsd = 'res_psdNew70'
        filenamecoh = 'res_cohNew70'
        ylimit = 4000
    elif mvc=='05':
        filenamepsd = 'res_psdNew05'
        filenamecoh = 'res_cohNew05'
        ylimit = 150
    figsFolder = '/home/pablo/git/master-thesis/figuras/'

    #****************************************
    #******* Calculating mean
    #****************************************
    simTypes = ['o', 'h', 's', 'd']
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
    fig, ax1 = plt.subplots()
    for simType in simTypes:
        # Here considering f was the same in all trials
        #import pdb; pdb.set_trace()
        # N.B. f[0] is supposed to be the same for all simTypes
        if not meanPSD[simType].any():
            continue
        ax1.plot(f[0][simType], 1e6*meanPSD[simType], symbols[simType], label=labels[simType])
    ax1.set_xlabel('Frequência (Hz)')
    ax1.set_ylabel('Densidade espectral de potência (mN$^2$)')
    ax1.grid()
    #plt.yscale('log')
    ax1.set_xlim([0, 50])
    ax1.set_ylim([0, ylimit])
    ax1.legend()
    # creating inset
    axInset = zoomed_inset_axes(ax1,
                    2,
                    loc=10)
    for simType in simTypes:
        if not meanPSD[simType].any():
            continue
        axInset.plot(f[0][simType], 1e6*meanPSD[simType], symbols[simType])
    mark_inset(ax1, axInset, loc1=2, loc2=3, fc="none", ec="0.5")
    axInset.set_xlim(8, 12)
    axInset.set_ylim(20, 80)
    #plt.show()
    plt.savefig(figsFolder + filenamepsd + '.svg', format='svg')

    plt.figure()
    for simType in simTypes:
        # Here considering f was the same in all trials
        if not meanCoh[simType].any():
            continue
        plt.plot(fc[0][simType], meanCoh[simType], symbols[simType], label=labels[simType])
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Coerência córtico-muscular')
    plt.grid()
    #     plt.yscale('log')
    plt.xlim([0, 50])
    #     plt.xlim((0, 500))
    plt.legend()
    #plt.show()
    plt.savefig(figsFolder + filenamecoh + '.svg', format='svg')

# These are conveniently converted to a numpy 2d array latter because singleTrial function return numpy arrays
numSubTrials = 10
psd = [{} for _ in range(1, numSubTrials+1)]
fpsd = [{} for _ in range(1, numSubTrials+1)]
coh = [{} for _ in range(1, numSubTrials+1)]
fc = [{} for _ in range(1, numSubTrials+1)]

print('Trials:\n - 1: step input\n - 2: sine input (very high amplitude)\n'
      ' - 3: All sine input same as 5% and with 5% amplitude\n'
      ' - 4: Same as 3 but with 1% amplitude\n'
      ' - 5: Same as 4 but s case not compensated')
trial = input('Trial number: ')
mvc = input('MVC percentage: ')
subtrials = [x for x in range(1, numSubTrials+1)]
for subtrial in subtrials:
    fpsd[subtrial-1], psd[subtrial-1], fc[subtrial-1], coh[subtrial-1] = singleTrial(trial, subtrial, str(mvc))

allTrials(psd, fpsd, coh, fc, str(mvc))
