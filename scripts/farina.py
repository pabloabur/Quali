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
    PBiPBni = {'o': [], 's': []}

    #****************************************
    #******* Running simulation for each case
    #****************************************
    for simType in simTypes:
        fileName = dataPath + '/spike' + simType + '.dat'
        #****************************************
        #******* Getting data
        #****************************************
        spikeTimes = []
        spikeUnits = []
        f = open(fileName, 'r')
        lines = f.readlines()
        for line in lines:
            spikeTimes.append(float(line.split()[0]))
            spikeUnits.append(float(line.split()[1]))
        f.close()

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

        fileName = dataPath + '/inspikes' + '.dat'
        inSpikeTimes = []
        inSpikeUnits = []
        f = open(fileName, 'r')
        lines = f.readlines()
        for line in lines:
            inSpikeTimes.append(float(line.split()[0]))
            inSpikeUnits.append(float(line.split()[1]))
        f.close()

        #****************************************
        #******* Preparing data
        #****************************************
        # Declaring variables needed for CST computation
        mnSpkTrain, rcSpkTrain  = np.zeros(len(t)), np.zeros(len(t))
        mnSpikes, rcSpikes = [], []

        # MN CST
        for i in range(5, 35, 1):
            auxSpks = [y for x, y in enumerate(spikeTimes) if spikeUnits[x]==i]
            mnSpikes = np.append(mnSpikes, auxSpks, axis=0)
        mnSpikes = np.sort(mnSpikes)
        for instant in mnSpikes:
            idx = int(round(instant/dt))
            mnSpkTrain[idx] = mnSpkTrain[idx] + 1
        # RC CST
        for i in range(10, 70, 1):
            auxSpks = [y for x, y in enumerate(inSpikeTimes) if inSpikeUnits[x]==i]
            rcSpikes = np.append(rcSpikes, auxSpks, axis=0)
        rcSpikes = np.sort(rcSpikes)
        for instant in rcSpikes:
            idx = int(round(instant/dt))
            rcSpkTrain[idx] = rcSpkTrain[idx] + 1

        # Relevant plots
        #plt.figure()
        #plt.plot(spikeTimes, spikeUnits, '.')
        #plt.title(simType)
        #plt.ylim([0, 150])
        #plt.xlabel('Tempo (ms)')
        #plt.ylabel('Índices dos neurônios')
        #plt.show()
        #plt.figure()
        #plt.plot(t, force, 'k')
        #plt.title(simType)
        #plt.xlabel('Tempo (ms)')
        #plt.ylabel('Força (N)')
        #plt.show()
        #plt.figure()
        #plt.plot(inSpikeTimes, inSpikeUnits, '.')
        #plt.title(simType)
        #plt.ylim([0, 700])
        #plt.xlabel('Tempo (ms)')
        #plt.ylabel('Índices dos neurônios')
        #plt.show()

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
        staticForce = [y for x,y in enumerate(force) if t[x]>tmin]
        staticForce = staticForce - np.mean(staticForce)
        filtForce = signal.filtfilt(b, a, staticForce)

        # Filter to compute CST
        fc = 10
        w = fc/fnyq
        b, a = signal.butter(4, w, 'low')
        rcCST = signal.filtfilt(b, a, rcSpkTrain)
        mnCST = signal.filtfilt(b, a, mnSpkTrain)

        staticMN = [y for x,y in enumerate(mnCST) if t[x]>tmin]
        staticMN = staticMN - np.mean(staticMN)
        staticRC = [y for x,y in enumerate(rcCST) if t[x]>tmin]
        staticRC = staticRC - np.mean(staticRC)
        staticFR = [y for x,y in enumerate(FR) if t[x]>tmin]
        staticFR = staticFR - np.mean(staticFR)
        taux = [y for x,y in enumerate(t) if t[x]>tmin]
        N = len(taux)

        #****************************************
        #******* Compare signals
        #****************************************
        #plt.figure()
        #plt.plot(taux, np.array(staticForce)/np.max(staticForce), label='raw force')
        #plt.plot(taux, np.array(filtForce)/np.max(filtForce), label='filtered force')
        #plt.plot(taux, np.array(staticMN)/np.max(staticMN), label='MN CST')
        #plt.plot(taux, np.array(staticRC)/np.max(staticRC), label='RC CST')
        #plt.plot(taux, np.array(staticFR)/np.max(staticFR), label='raw input')
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
        # Measures
        A0 = np.abs(yfi[indexW0])
        A1 = np.abs(yfi[indexW1])
        A2 = np.abs(yfi[indexW2])
        B0 = np.abs(yfo[indexW0])
        B1 = np.abs(yfo[indexW1])
        B2 = np.abs(yfo[indexW2])
        B1B2[simType] = B0/B1
        B1B3[simType] = B0/B2
        # Remove intervals outside 0-6 Hz
        Bni = [yfo[y] for y, x in enumerate(ff) if (x>=0.0 and x<=6.0)]
        ffaux = [ff[y] for y, x in enumerate(ff) if (x>=0.0 and x<=6.0)]
        indexW0 = [y for y, x in enumerate(ffaux) if np.isclose(x, 0.5, atol=1e-3)][0]
        indexW1 = [y for y, x in enumerate(ffaux) if np.isclose(x, 1.0, atol=1e-3)][0]
        indexW2 = [y for y, x in enumerate(ffaux) if np.isclose(x, 2.5, atol=1e-3)][0]
        # Remove harmonic peaks
        harmonics = [indexW0, indexW1, indexW2]
        Bni = [np.abs(x)**2 if y not in harmonics else 0.0 for y, x in enumerate(Bni)]
        PBiPBni[simType] = np.sqrt(B0**2+B1**2+B2**2)/np.sqrt(np.sum(np.array(
            Bni)**2))

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
        #print('*** Power of all peaks')

        #print('sqrt(B0^2+B1^2+B2^2)/sum(B!=0,1,2) = {:.6f}'.format(
        #    PBiPBni[simType]))

        #plt.figure()
        #plt.plot(ff, np.abs(yfo), 'ko', label='force')
        #plt.vlines(ff, 0, np.abs(yfo))
        #plt.plot(ff, np.abs(yfi), 'rx', label='input')
        #plt.vlines(ff, 0, np.abs(yfi), color='r', linestyles='dashed')
        #plt.plot(ffaux, Bni, 'bx', label='force FFT w/o main harmonics')
        #plt.title(simType)
        #plt.xlabel('f (Hz)')
        #plt.ylabel('FFT')
        #plt.xlim([0, 6])
        #plt.legend()
        #plt.grid()
        #plt.show()

        out[simType] = np.abs(yfo)
    return out, ff, B1B2, B1B3, PBiPBni

figsFolder = '/home/pablo/git/master-thesis/figuras/'
subTrials = 30
ffto = {'o': [[] for i in range(subTrials)], 's': [[] for i in range(subTrials)]}
b1b2 = {'o': [[] for i in range(subTrials)], 's': [[] for i in range(subTrials)]}
b1b3 = {'o': [[] for i in range(subTrials)], 's': [[] for i in range(subTrials)]}
pbipbni = {'o': [[] for i in range(subTrials)], 's': [[] for i in range(subTrials)]}
f = []

for subTrial in range(1, subTrials+1):
    print('running subtrial {}'.format(subTrial))
    auxo, f, auxb1, auxb2, auxp = singleTrial(subTrial)
    for k, val in auxo.items():
        ffto[k][subTrial-1] = val
    for k, val in auxb1.items():
        b1b2[k][subTrial-1] = val
    for k, val in auxb2.items():
        b1b3[k][subTrial-1] = val
    for k, val in auxp.items():
        pbipbni[k][subTrial-1] = val

print('mean q1 without RC = {:.1f}'.format(np.mean(b1b2['o'])))
print('mean q1 with RC = {:.1f}'.format(np.mean(b1b2['s'])))
print('mean q2 without RC = {:.1f}'.format(np.mean(b1b3['o'])))
print('mean q2 with RC = {:.1f}'.format(np.mean(b1b3['s'])))
print('mean q3 without = {:.6f}'.format(np.mean(pbipbni['o'])))
print('mean q3 with = {:.6f}'.format(np.mean(pbipbni['s'])))

#import pdb; pdb.set_trace()
# Use following index to select a plot from a trial
idx = 5
plt.figure()
plt.plot(f, ffto['o'][idx], 'ko', label='Sem CR')
plt.vlines(f, 0, ffto['o'][idx], color='k')
plt.plot(f, ffto['s'][idx], 'rx', label='Com CR')
plt.vlines(f, 0, ffto['s'][idx], color='r')
plt.xlabel('frequência (Hz)')
plt.ylabel('Módulo da transformada de fourier da força')
plt.xlim([0, 7])
plt.legend()
plt.grid()
#plt.show()
plt.savefig(figsFolder + 'res_fft' + '.svg', format='svg')
