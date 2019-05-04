import matplotlib
#matplotlib.use('TkAgg') # For X11 forwarding
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
import numpy as np
from scipy import signal

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
        # Inputs plots
        labels = {'rc': 'Entradas inibitórias', 'dc': 'Entradas excitatórias'}
        symbols = {'rc': 'k', 'dc': 'k--'}

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

    #for simType in simTypes:
    #    plt.figure()
    #    plt.plot(t, gsyn[simType], symbols[simType], label=labels[simType])
    #    plt.legend()
    #    plt.xlabel('Tempo (ms)')
    #    plt.ylabel('Voltagem (mV)')
    #    plt.grid()

    #print('Mean conductance, in module, is {:.2f}'.format(abs(np.mean(
    #   gsyn['dc']))))

    #****************************************
    #******* Computing PSD and coherences
    #****************************************
    fr = 1
    nperseg = 4*fs/2/fr
    noverlap = None
    nfft = None#8*nperseg
    #detrend = 'constant'
    detrend = False
    #detrend = 'linear'
    scale = 'spectrum'

    limits = {'rc': 0.0002, 'dc': 1}
    for simType in simTypes:
        # Plot inputs PSD
        ff, PSD = signal.welch(gsyn[simType], fs, 'hann', nperseg, noverlap,
                nfft, detrend, scaling = scale)
        #plt.figure()
        #plt.plot(ff, PSD, symbols[simType], label=labels[simType])
        #plt.ylim([0, limits[simType]])
        #plt.xlim([0, 50])
        #plt.legend()
        #plt.xlabel('Frequência (Hz)')
        #plt.ylabel('Densidade espectral de potência (mN$^2$)')
        #plt.grid()

    # Plot coherence between inputs
    # Here is higher than in example because I needed more resolution to
    # compare f to 10 Hz
    nperseg = 20000
    fc, coherence = signal.coherence(gsyn['rc'], gsyn['dc'], fs, 'hann',
                                     nperseg, noverlap, nfft, detrend)
    #plt.figure()
    #print('nsamples: {:}'.format(len(gsyn['rc'])))
    #print('nperseg: {:}'.format(nperseg))
    #print('nwindows: {:.1f}'.format(len(gsyn['rc'])/nperseg))
    #import pdb; pdb.set_trace()
    #plt.plot(fc, coherence, symbols[simType], label=labels[simType])
    #plt.xlabel('Frequência (Hz)')
    #plt.ylabel('Coerência córtico-muscular')
    #plt.grid()
    #plt.xlim([0, 50])
    #plt.legend()

    # cross spectral density used to study coherence phase
    _, crossSpectrum = signal.csd(gsyn['rc'], gsyn['dc'], fs, 'hann',
                                     nperseg, noverlap, nfft, detrend)
    crossSpectrum = np.angle(crossSpectrum, deg=False)
    # Cross spectral density plot
    #plt.figure()
    #plt.plot(fc, crossSpectrum, 'k')
    #plt.xlabel('Frequência (Hz)')
    #plt.ylabel('Pxy fase (graus)')
    #plt.grid()
    #plt.xlim([0, 50])
    #plt.show()

    return fc, crossSpectrum

def exampleTrial():
    #****************************************
    #******* Simulation settings and variables
    #****************************************
    # Simulation
    duration = 11000
    tmin = 1000
    dt = 0.05
    simTypes = ['dc', 'rc']
    fs=1/(dt*1e-3)
    gsyn = {'dc': [], 'rc': []}
    vm = {'dc': [], 'rc': []}

    # Files and paths
    figsFolder = '/home/pablo/git/master-thesis/figuras/'
    dataPathVm = '/home/pablo/osf/Master-Thesis-Data/population/psd/cancel/trial2/trial1'
    dataPathGs = '/home/pablo/osf/Master-Thesis-Data/population/psd/cancel/trial1/trial1'

    #****************************************
    #******* Running simulation for each case
    #****************************************
    for j, simType in enumerate(simTypes):
        # Variables calculated
        gsynSOL = []
        vmSOL = []
        taux = []
        # Inputs plots
        labels = {'rc': 'Entradas inibitórias', 'dc': 'Entradas excitatórias'}
        symbols = {'rc': 'k', 'dc': 'k--'}

        #****************************************
        #******* Getting and processing for analysis
        #****************************************
        fileName = dataPathGs + '/gsyn' + simType + '.dat'
        f = open(fileName, 'r')
        lines = f.readlines()
        for line in lines:
            taux.append(float(line.split()[0]))
            gsynSOL.append(float(line.split()[2]))
        f.close()
        fileName = dataPathVm + '/gsyn' + simType + '.dat'
        f = open(fileName, 'r')
        lines = f.readlines()
        for line in lines:
            vmSOL.append(float(line.split()[2]))
        f.close()

        #****************************************
        #******* Gathering data for latter use
        #****************************************
        staticInputG = [y for x,y in enumerate(gsynSOL) if taux[x]>tmin]
        staticInputV = [y for x,y in enumerate(vmSOL) if taux[x]>tmin]
        t = [y for x,y in enumerate(taux) if taux[x]>tmin]
        gsyn[simType] = staticInputG
        vm[simType] = staticInputV

    #****************************************
    #******* Computing PSD and coherences
    #****************************************
    fr = 1
    nperseg = 4*fs/2/fr
    noverlap = None
    nfft = None#8*nperseg
    detrend = False
    scale = 'spectrum'

    # Gsyn psd plots
    fig, ax1 = plt.subplots()
    for simType in simTypes:
        # Plot inputs PSD
        ff, PSD = signal.welch(gsyn[simType], fs, 'hann', nperseg, noverlap,
                nfft, detrend, scaling = scale)
        ax1.plot(ff, 1e6*PSD, symbols[simType])
    ax1.set_ylim([0, 700])
    ax1.set_xlim([0, 50])
    ax1.set_xlabel('Frequência (Hz)')
    ax1.set_ylabel('Densidade espectral de potência da força (N$^2$)')
    # creating inset
    axInset = zoomed_inset_axes(ax1,
                    8,
                    loc=10)
    axInset.plot(ff, 1e6*PSD, symbols[simType])
    mark_inset(ax1, axInset, loc1=4, loc2=3, fc="none", ec="0.5")
    axInset.set_xlim(9, 11)
    axInset.set_ylim(0, 15)
    plt.savefig(figsFolder + 'res_gsynpsdex' + '.svg', format='svg')
    #plt.show()
    # Vm psd plots
    fig, ax2 = plt.subplots()
    for simType in simTypes:
        # Plot inputs PSD
        ff, PSD = signal.welch(vm[simType], fs, 'hann', nperseg, noverlap,
                nfft, detrend, scaling = scale)
        plt.plot(ff, PSD, symbols[simType])
    ax2.set_ylim([0, .5])
    ax2.set_xlim([0, 50])
    ax2.set_xlabel('Frequência (Hz)')
    ax2.set_ylabel('Densidade espectral de potência da força (N$^2$)')
    # creating inset
    axInset = zoomed_inset_axes(ax2,
                    8,
                    loc=10)
    axInset.plot(ff, PSD, symbols[simType])
    mark_inset(ax2, axInset, loc1=4, loc2=3, fc="none", ec="0.5")
    axInset.set_xlim(9, 11)
    axInset.set_ylim(0, 0.003)
    plt.savefig(figsFolder + 'res_vmpsdex' + '.svg', format='svg')
    #plt.show()

    # Plot coherence between inputs (gsyn only)
    plt.figure()
    nperseg = 15000
    fc, coherence = signal.coherence(gsyn['rc'], gsyn['dc'], fs, 'hann',
                                     nperseg, noverlap, nfft, detrend)
    plt.plot(fc, coherence, symbols[simType])
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Módulo da coerência córtico-muscular')
    plt.grid()
    plt.xlim([0, 50])
    plt.savefig(figsFolder + 'res_gsyncohex' + '.svg', format='svg')
    #plt.show()

    # cross spectral density used to study coherence phase
    _, crossSpectrum = signal.csd(gsyn['rc'], gsyn['dc'], fs, 'hann',
                                     nperseg, noverlap, nfft, detrend)
    # Cross spectral density plot
    fig, ax4 = plt.subplots()
    ax4.plot(fc, np.angle(crossSpectrum, deg=False), 'k')
    ax4.set_xlabel('Frequência (Hz)')
    ax4.set_ylabel('Fase da coerência córtico-muscular (rad)')
    ax4.grid()
    ax4.set_xlim([0, 50])
    # setting ticks to pi
    fc_tick = np.arange(-1, 2)
    y_label = ['$-\pi$', '0', '$\pi$']
    ax4.set_yticks(fc_tick*np.pi)
    ax4.set_yticklabels(y_label)
    plt.savefig(figsFolder + 'res_gsyncsdex' + '.svg', format='svg')
    #plt.show()

def allTrials(PSDs, f, nTrials, figName):
    # Files and paths
    figsFolder = '/home/pablo/git/master-thesis/figuras/'

    #****************************************
    #******* Plotting
    #****************************************
    fig, ax = plt.subplots()
    psdAt10 = [y for trialPSD in PSDs for x, y in enumerate(trialPSD) if f[0][x]==10]
    # N.B. f[0] is supposed to be the same for all trials
    ax.plot([10 for _ in range(nTrials)], psdAt10, 'ko', fillstyle='none')
    ax.set_xlabel('Frequência (Hz)')
    ax.set_ylabel('Fase da coerência córtico-muscular (rad)')
    # setting ticks to pi
    f_tick = np.arange(-1, 2)
    y_label = ['$-\pi$', '0', '$\pi$']
    ax.set_yticks(f_tick*np.pi)
    ax.set_yticklabels(y_label)
    #plt.show()
    plt.savefig(figsFolder + 'res_csds' + figName + '.svg', format='svg')

# These are conveniently converted to a numpy 2d array latter because singleTrial function return numpy arrays
numSubTrials = 10
psd = [[] for _ in range(1, numSubTrials+1)]
fpsd = [[] for _ in range(1, numSubTrials+1)]

print('Using first trial as example')
exampleTrial()

print('Trials:\n - 1: gsyn\n - 2: vm\n')
trial = input('Trial number: ')
subtrials = [x for x in range(1, numSubTrials+1)]
for subtrial in subtrials:
    fpsd[subtrial-1], psd[subtrial-1], = singleTrial(trial, subtrial)

if trial=='1':
    figName = 'gsyn'
else:
    figName = 'vm'
allTrials(psd, fpsd, numSubTrials, figName)
