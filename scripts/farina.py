import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal, integrate
from scipy.fftpack import fft, fftshift, fftfreq

def singleTrial(subTrial):
    ###### File settings
    dataPath = '/home/pablo/osf/Master-Thesis-Data/population/farina/trial1/trial' + str(subTrial)
    duration = 10000
    tmin = 2000
    dt = 0.05
    t = np.arange(0, duration, dt)
    fs=1/(dt*1e-3)
    simTypes = ['o', 's']
    out = {'o': [], 's': []}
    B1B2 = {'o': [], 's': []}
    B1B3 = {'o': [], 's': []}
    PBiB0 = {'o': [], 's': []}
    PBiPBni = {'o': [], 's': []}
    window = signal.windows.hann(int(400/dt))
    windowArea = integrate.trapz(window, dx = dt)
    normWindow = window/windowArea*1e3 # 1e3 multiplied because area was in mili

    #****************************************
    #******* Running simulation for each case
    #****************************************
    for simType in simTypes:
        fileName = dataPath + '/spike' + simType + '.dat'
        #****************************************
        #******* Getting and processing spike data
        #****************************************
        spikeTimes = []
        spikeUnits = []
        f = open(fileName, 'r')
        lines = f.readlines()
        for line in lines:
            spikeTimes.append(float(line.split()[0]))
            spikeUnits.append(float(line.split()[1]))
        f.close()
        # This part to show some examples of how MNs are firing
        #plt.figure()
        #plt.plot(spikeTimes, spikeUnits, '.')
        #plt.title(simType)
        #plt.ylim([0, 150])
        #plt.xlabel('Tempo (ms)')
        #plt.ylabel('Índices dos neurônios')
        #plt.show()

        #****************************************
        #******* Getting and processing force data
        #****************************************
        t = []
        taux = []
        dendPot = []
        force = []
        FR = []
        fileName = dataPath + '/inout' + simType + '.dat'
        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            for line in lines:
                t.append(float(line.split()[0]))
                dendPot.append(float(line.split()[1]))
                force.append(float(line.split()[2]))
                FR.append(float(line.split()[3]))
            f.close()
        except:
            print('Warning: File ' + fileName + ' could not be opened.')

        # Extract values after tmin
        staticForce = [y for x,y in enumerate(force) if t[x]>tmin]
        print(np.mean(staticForce))
        staticForce = staticForce - np.mean(staticForce)
        staticFR = [y for x,y in enumerate(FR) if t[x]>tmin]
        staticFR = staticFR - np.mean(staticFR)
        taux = [y for x,y in enumerate(t) if t[x]>tmin]
        N = len(taux)

        # Plots of generated force
        #plt.figure()
        #plt.plot(t, force, 'k')
        #plt.title(simType)
        #plt.xlabel('Tempo (ms)')
        #plt.ylabel('Força (N)')
        #plt.show()

        #****************************************
        #******* Plot RC response and compare to force
        #****************************************
        if (subTrial == 1 or subTrial == 2) and (simType == 's'):
            fileName = dataPath + '/inspike' + simType + '.dat'
            inSpikeTimes = []
            inSpikeUnits = []
            f = open(fileName, 'r')
            lines = f.readlines()
            for line in lines:
                inSpikeTimes.append(float(line.split()[0]))
                inSpikeUnits.append(float(line.split()[1]))
            f.close()

            # Plot used for more detailed investigation
            #plt.figure()
            #plt.plot(inSpikeTimes, inSpikeUnits, '.')
            #plt.title(simType)
            #plt.ylim([0, 700])
            #plt.xlabel('Tempo (ms)')
            #plt.ylabel('Índices dos neurônios')
            #plt.show()

            # Processing RC response
            rcFiringRate = np.array([])
            inSpkTrain = np.zeros(len(t))
            # Processing MN response
            mnFiringRate = np.array([])
            mnSpkTrain = np.zeros(len(t))

            # Low pass filter
            b, a = signal.butter(4, 2/fnyq, 'low')
            # Plot CST filter
            #w, h = signal.freqz(b, a, worN=10000)
            #plt.figure()
            #plt.plot(fnyq*w/np.pi, abs(h))
            #plt.title('Filter frequency response')
            #plt.xlim([0, 20])
            #plt.show()

            # Calculate instantaneous firing rate
            # RCs
            rcSpikes = [y for x, y in enumerate(inSpikeTimes) if inSpikeUnits[x]==180]
            for instant in rcSpikes:
                inSpkTrain[int(instant/dt)] = 1
            rcFiringRate = signal.lfilter(b, a, inSpkTrain)
            #rcFiringRate = signal.convolve(inSpkTrain, normWindow, mode = 'same')

            # MNs
            mnSpikes = []
            for i in range(80, 110, 1):
                auxSpks = [y for x, y in enumerate(spikeTimes) if spikeUnits[x]==i]
                mnSpikes = np.append(mnSpikes, auxSpks, axis=0)
            mnSpikes = np.sort(mnSpikes)
            for instant in mnSpikes:
                mnSpkTrain[int(instant/dt)] = 1
            mnFiringRate = signal.lfilter(b, a, mnSpkTrain)
            #mnFiringRate = signal.convolve(mnSpkTrain, normWindow, mode = 'same')

            staticRC = [y for x,y in enumerate(rcFiringRate) if t[x]>tmin]
            staticRC = staticRC - np.mean(staticRC)
            staticMN = [y for x,y in enumerate(mnFiringRate) if t[x]>tmin]
            staticMN = staticMN - np.mean(staticMN)

            plt.figure()
            plt.plot(taux, np.array(staticForce)/np.max(staticForce), label='raw output')
            plt.plot(taux, np.array(staticRC)/np.max(staticRC), label='RC output')
            plt.plot(taux, np.array(staticMN)/np.max(staticMN), label='MN output')
            plt.legend()
            plt.title(simType)
            plt.xlabel('t (ms)')
            plt.grid()
            plt.show()
        #****************************************
        #******* Filter desings and signal processing
        #****************************************
        # Filter to smooth muscle force
        fc = 7
        fnyq = fs/2
        w = fc/fnyq
        b, a = signal.butter(4, w, 'low')
        # Plot filter frequency response
        #w, h = signal.freqz(b, a, worN=10000)
        #plt.figure()
        #plt.plot(fnyq*w/np.pi, abs(h))
        #plt.title('Filter frequency response')
        #plt.xlim([0, 20])
        #plt.show()
        filtForce = signal.lfilter(b, a, staticForce)

#_____________________________________
        b, a = signal.butter(4, 10/fnyq, 'low')
        mnSpkTrain = np.zeros(len(t))
        mnSpikes = []
        for i in range(81, 110, 1):
            auxSpks = [y for x, y in enumerate(spikeTimes) if spikeUnits[x]==i]
            mnSpikes = np.append(mnSpikes, auxSpks, axis=0)
        mnSpikes = np.sort(mnSpikes)
        for instant in mnSpikes:
            mnSpkTrain[int(instant/dt)] = 1
        mnFiringRate = signal.lfilter(b, a, mnSpkTrain)
        #mnFiringRate = signal.convolve(mnSpkTrain, normWindow, mode = 'same')

        #staticRC = [y for x,y in enumerate(rcFiringRate) if t[x]>tmin]
        #staticRC = staticRC - np.mean(staticRC)
        staticMN = [y for x,y in enumerate(mnFiringRate) if t[x]>tmin]
        staticMN = staticMN - np.mean(staticMN)

        plt.figure()
        plt.plot(taux, np.array(staticForce)/np.max(staticForce), label='raw output')
        plt.plot(taux, np.array(staticMN)/np.max(staticMN), label='raw output')
        plt.legend()
        plt.title(simType)
        plt.xlabel('t (ms)')
        plt.grid()
        plt.show()
#_____________________________________

        #****************************************
        #******* Compare signals
        #****************************************
        #plt.figure()
        #plt.plot(taux, np.array(filtForce)/np.max(filtForce), label='filtered output')
        #plt.plot(taux, np.array(staticFR)/np.max(staticFR), label='raw input')
        #plt.plot(taux, np.array(staticForce)/np.max(staticForce), label='raw output')
        #plt.legend()
        #plt.title(simType)
        #plt.xlabel('t (ms)')
        #plt.grid()
        #plt.show()

        #****************************************
        #******* Performing FFT on signals
        #****************************************
        yfo = fft(filtForce)
        yfo = fftshift(yfo)
        yfi = fft(staticFR)
        yfi = fftshift(yfi)
        ff = fftfreq(N, 1/fs)
        ff = fftshift(ff)

        #****************************************
        #******* Retrieving peak values
        #****************************************
        # Finding indexes of harmonics
        indexW0 = [y for y, x in enumerate(ff) if np.isclose(x, 0.5, atol=1e-3)][0]
        indexW1 = [y for y, x in enumerate(ff) if np.isclose(x, 1.0, atol=1e-3)][0]
        indexW2 = [y for y, x in enumerate(ff) if np.isclose(x, 2.5, atol=1e-3)][0]
        indexW0n = [y for y, x in enumerate(ff) if np.isclose(x, -0.5, atol=1e-3)][0]
        indexW1n = [y for y, x in enumerate(ff) if np.isclose(x, -1.0, atol=1e-3)][0]
        indexW2n = [y for y, x in enumerate(ff) if np.isclose(x, -2.5, atol=1e-3)][0]
        # Measures
        A0 = np.abs(yfi[indexW0])
        A1 = np.abs(yfi[indexW1])
        A2 = np.abs(yfi[indexW2])
        B0 = np.abs(yfo[indexW0])
        B1 = np.abs(yfo[indexW1])
        B2 = np.abs(yfo[indexW2])
        B1B2[simType] = B0/B1
        B1B3[simType] = B0/B2
        PBiB0[simType] = np.sqrt(B0**2+B1**2+B2**2)/B0

        # Print measures
        #print('******** {} Proportions ********'.format(simType))
        #print('*** peak0/peakX')
        #print('A0/A1 = {:.2f}'.format(A0/A1))
        #print('A0/A2 = {:.2f}'.format(A0/A2))
        #print('B0/B1 = {:.2f}'.format(B1B2[simType]))
        #print('B0/B2 = {:.2f}'.format(B1B3[simType]))
        #print('*** Power of harmonic peaks')
        #print('sqrt(A0^2+A1^2+A2^2)/A0 = {:.2f}'.format(
        #    np.sqrt(A0**2+A1**2+A2**2)/A0))
        #print('sqrt(B0^2+B1^2+B2^2)/B0 = {:.2f}'.format(PBiB0[simType]))
        #print('*** Power of all peaks')
        indexes = [indexW0, indexW1, indexW2, indexW0n, indexW1n, indexW2n]
        # Remove harmonic peaks
        Bni = [np.abs(x)**2 if y not in indexes else 0.0 for y, x in enumerate(yfo)]
        # Remove negative part
        Bni = [x if y>=len(Bni)//2 else 0.0 for y, x in enumerate(Bni)]
        PBiPBni[simType] = np.sqrt(B0**2+B1**2+B2**2)/np.sqrt(np.sum(np.array(
            Bni)**2))
        #print('sqrt(B0^2+B1^2+B2^2)/sum(B!=0,1,2) = {:.2f}'.format(
        #    PBiPBni[simType]))

        #plt.figure()
        #plt.plot(ff, np.abs(yfo), 'ko', label='force')
        #plt.vlines(ff, 0, np.abs(yfo))
        ##plt.plot(ff, np.sqrt(Bni), 'bx', label='force w/o main harmonics')
        #plt.plot(ff, np.abs(yfi), 'rx', label='input')
        #plt.vlines(ff, 0, np.abs(yfi), color='r', linestyles='dashed')
        #plt.title(simType)
        #plt.xlabel('f (Hz)')
        #plt.ylabel('FFT')
        #plt.xlim([0, 10])
        #plt.legend()
        #plt.grid()
        #plt.show()

        out[simType] = np.abs(yfo)
        #import pdb; pdb.set_trace()
    return out, ff, B1B2, B1B3, PBiB0, PBiPBni

subTrials = 10
ffto = {'o': [[] for i in range(subTrials)], 's': [[] for i in range(subTrials)]}
b1b2 = {'o': [[] for i in range(subTrials)], 's': [[] for i in range(subTrials)]}
b1b3 = {'o': [[] for i in range(subTrials)], 's': [[] for i in range(subTrials)]}
pbib0 = {'o': [[] for i in range(subTrials)], 's': [[] for i in range(subTrials)]}
pbipbni = {'o': [[] for i in range(subTrials)], 's': [[] for i in range(subTrials)]}
f = []

for subTrial in range(1, subTrials+1):
    print('running subtrial {}'.format(subTrial))
    auxo, f, auxb1, auxb2, auxp1, auxp2 = singleTrial(subTrial)
    for k, val in auxo.items():
        ffto[k][subTrial-1] = val
    for k, val in auxb1.items():
        b1b2[k][subTrial-1] = val
    for k, val in auxb2.items():
        b1b3[k][subTrial-1] = val
    for k, val in auxp1.items():
        pbib0[k][subTrial-1] = val
    for k, val in auxp2.items():
        pbipbni[k][subTrial-1] = val

idx = 0
while True:
    plt.figure()
    plt.plot(f, ffto['o'][idx], 'ko', label='Sem CR')
    plt.vlines(f, 0, ffto['o'][idx], color='k')
    plt.plot(f, ffto['s'][idx], 'rx', label='Com CR')
    plt.vlines(f, 0, ffto['s'][idx], color='r')
    plt.xlabel('f (Hz)')
    plt.ylabel('FFT')
    plt.xlim([0, 10])
    plt.legend()
    plt.grid()
    plt.show()
