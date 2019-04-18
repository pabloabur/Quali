import matplotlib
#matplotlib.use('TkAgg') # For X11 forwarding
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.fftpack import fft

from ensembleRate import ensembleFR

def singleTrial(trial, subTrial):
    #****************************************
    #******* Simulation settings and variables
    #****************************************
    # Simulation
    duration = 11000
    tmin = 1000
    dt = 0.05
    simTypes = ['dc', 'rc']
    fs=1/(dt*1e-3)

    # Files and paths
    dataPath = ('/home/pablo/osf/Master-Thesis-Data/population/psd/cancel/trial'
                + str(trial) + '/trial' + str(subtrial))

    gsyn = {'dc': [], 'rc': []}

    #****************************************
    #******* Running simulation for each case
    #****************************************
    for j, simType in enumerate(simTypes):
        # Variables calculated
        gsynMG = []
        gsynSOL = []
        taux = []

        #****************************************
        #******* Getting and processing for analysis
        #****************************************
        fileName = dataPath + '/gsyn' + simType + '.dat'
        f = open(fileName, 'r')
        lines = f.readlines()
        for line in lines:
            # RC effect
            taux.append(float(line.split()[0]))
            gsynMG.append(float(line.split()[1]))
            gsynSOL.append(float(line.split()[2]))
        f.close()

        # Membrane potentials from pools and EMG
        #plt.figure()
        #plt.plot(gsynMG, label='MG')
        #plt.plot(gsynSOL, label='SOL')
        #plt.legend()
        #plt.title(simType)
        #plt.show()
        
        #****************************************
        #******* Gathering data for latter use
        #****************************************
        staticInput = [y for x,y in enumerate(gsynSOL) if taux[x]>tmin]
        t = [y for x,y in enumerate(taux) if taux[x]>tmin]
        gsyn[simType] = staticInput

    labels = {'rc': 'Entradas inibitórias', 'dc': 'Entradas excitatórias'}
    symbols = {'rc': 'k', 'dc': 'k--'}
    for simType in simTypes:
        plt.figure()
        plt.plot(t, gsyn[simType], symbols[simType], label=labels[simType])
        plt.legend()
        plt.xlabel('Tempo (ms)')
        plt.ylabel('Voltagem (mV)')
        plt.grid()

    #print('Mean conductance, in module, is {:.2f}'.format(abs(np.mean(
    #   gsyn['dc']))))

    #****************************************
    #******* Computing PSD and coherences
    #****************************************
    fr = 1
    nperseg = 4*fs/2/fr
    noverlap = 0#None
    nfft = None#8*nperseg
    #detrend = 'constant'
    detrend = False
    #detrend = 'linear'
    scale = 'spectrum'

    limits = {'rc': 0.0002, 'dc': 1}
    for simType in simTypes:
        plt.figure()
        ff, PSD = signal.welch(gsyn[simType], fs, 'hann', nperseg, noverlap,
                nfft, detrend, scaling = scale)
        plt.plot(ff, PSD, symbols[simType], label=labels[simType])
        plt.ylim([0, limits[simType]])
        plt.xlim([0, 50])
        plt.legend()
        plt.xlabel('Frequência (Hz)')
        plt.ylabel('Densidade espectral de potência (mN$^2$)')
        plt.grid()

    plt.figure()
    nperseg = 8000
    print('nsamples: {:}'.format(len(gsyn['rc'])))
    print('nperseg: {:}'.format(nperseg))
    print('nwindows: {:.1f}'.format(len(gsyn['rc'])/nperseg))
    # Coherence estimate
    fc, coherence = signal.coherence(gsyn['rc'], gsyn['dc'], fs, 'hann',
                                     nperseg, noverlap, nfft, detrend)
    plt.plot(fc, coherence, symbols[simType], label=labels[simType])
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Coerência córtico-muscular')
    plt.grid()
    plt.xlim([0, 50])
    plt.legend()
    # cross spectral density used to study coherence phase
    _, crossSpectrum = signal.csd(gsyn['rc'], gsyn['dc'], fs, 'hann',
                                     nperseg, noverlap, nfft, detrend)
    plt.figure()
    plt.plot(fc, np.angle(crossSpectrum, deg=True), 'k')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Pxy fase (graus)')
    plt.grid()
    plt.xlim([0, 50])
    plt.show()

# Here as an example
#def allTrials(PSDs, f, Coherences, fc):
#    # Files and paths
#    filenamepsd = 'res_psdNew05'
#    filenamecoh = 'res_cohNew05'
#    figsFolder = '/home/pablo/git/master-thesis/figuras/'
#
#    #****************************************
#    #******* Calculating mean
#    #****************************************
#    simTypes = ['o', 's']
#    symbols = {'d': 'k', 's': 'k--', 'h': 'k-.', 'o': 'k:'}
#    meanPSD = {'d': [], 's': [], 'h': [], 'o': []}
#    meanCoh = {'d': [], 's': [], 'h': [], 'o': []}
#    labels = {'d': 'Forte', 's': 'Normal', 'h': 'Fraco', 'o': 'Ausente'}
#    for simType in simTypes:
#        meanPSD[simType] = np.mean([PSD[simType] for PSD in PSDs], axis=0)
#        meanCoh[simType] = np.mean([coh[simType] for coh in Coherences], axis=0)
#
#    #****************************************
#    #******* Plotting
#    #****************************************
#    plt.figure()
#    for simType in simTypes:
#        # Here considering f was the same in all trials
#        plt.plot(f[0]['o'], 1e6*meanPSD[simType], symbols[simType], label=labels[simType])
#    plt.xlabel('Frequência (Hz)')
#    plt.ylabel('Densidade espectral de potência (mN$^2$)')
#    plt.grid()
#    #plt.yscale('log')
#    plt.xlim([0, 50])
#    plt.ylim([0, 8000])
#    plt.legend()
#    plt.show()
#    #plt.savefig(figsFolder + filenamepsd + '.svg', format='svg')
#
#    plt.figure()
#    for simType in simTypes:
#        # Here considering f was the same in all trials
#        plt.plot(fc[0]['o'], meanCoh[simType], symbols[simType], label=labels[simType])
#    plt.xlabel('Frequência (Hz)')
#    plt.ylabel('Coerência córtico-muscular')
#    plt.grid()
#    #     plt.yscale('log')
#    plt.xlim([0, 50])
#    #     plt.xlim((0, 500))
#    plt.legend()
#    plt.show()
#    #plt.savefig(figsFolder + filenamecoh + '.svg', format='svg')

# These are conveniently converted to a numpy 2d array latter because singleTrial function return numpy arrays
# TODO make it 10
numSubTrials = 9
psd = [[] for _ in range(1, numSubTrials+1)]
fpsd = [[] for _ in range(1, numSubTrials+1)]
coh = [[] for _ in range(1, numSubTrials+1)]
fc = [[] for _ in range(1, numSubTrials+1)]
reduc = [[] for _ in range(1, numSubTrials+1)]
syncs = [[] for _ in range(1, numSubTrials+1)]

trial = input('Trial number: ')
subtrials = [x for x in range(1, numSubTrials+1)]
for subtrial in subtrials:
    singleTrial(trial, subtrial)
