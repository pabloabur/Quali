import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal, integrate
from scipy.fftpack import fft, fftshift, fftfreq

###### File settings
dataPath = '/home/pablo/osf/Master-Thesis-Data/population/farina/trial1/trial3/'
duration = 10000
tmin = 2000
dt = 0.05
t = np.arange(0, duration, dt)
fs=1/(dt*1e-3)
simTypes = ['o', 's']
out = {'o': [], 's': []}

#****************************************
#******* Running simulation for each case
#****************************************
for i, simType in enumerate(simTypes):
    fileName = dataPath + '/spike' + simType + '.dat'
    #****************************************
    #******* Getting and processing spike data
    #****************************************
    spikeTimes = []
    spikeUnits = []
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

    # Plot used for more detailed investigation
    #plt.figure()
    #plt.plot(spikeTimes, spikeUnits, '.')
    #plt.title(simType)
    #plt.ylim([0, 150])
    #plt.xlabel('Tempo (ms)')
    #plt.ylabel('Índices dos MNs')
    #plt.show()

    #****************************************
    #******* Getting and processing force data
    #****************************************
    taux = []
    dendPot = []
    force = []
    FR = []
    fileName = dataPath + '/inout' + simType + '.dat'
    try:
        f = open(fileName, 'r')
        lines = f.readlines()
        for line in lines:
            taux.append(float(line.split()[0]))
            dendPot.append(float(line.split()[1]))
            force.append(float(line.split()[2]))
            FR.append(float(line.split()[3]))
        f.close()
    except:
        print('Warning: File ' + fileName + ' could not be opened.')

    # Extract values after tmin
    staticForce = [y for x,y in enumerate(force) if taux[x]>tmin]
    staticForce = staticForce - np.mean(staticForce)
    staticFR = [y for x,y in enumerate(FR) if taux[x]>tmin]
    staticFR = staticFR - np.mean(staticFR)
    taux = [y for x,y in enumerate(taux) if taux[x]>tmin]
    N = len(taux)

    # design filter
    fc = 7
    fnyq = fs/2
    w = fc/fnyq
    b, a = signal.butter(4, w, 'low')
    # Plot filter frequency response
    #w, h = signal.freqz(b, a)
    #plt.figure()
    #plt.plot(fs*w, 20*np.log10(abs(h)))
    #plt.title('Filter frequency response')
    #plt.xlim([0, 10])
    #plt.ylim([-15, 0])
    #plt.show()
    # Filter signal (force)
    filtSignal = signal.lfilter(b, a, staticForce)

    # Creating the CST
    #import pdb; pdb.set_trace()
    spkTrain = np.sort(spikeTimes)
    # Plot the CST
    #fig, ax = plt.subplots()
    #ax.plot((spkTrain, spkTrain), (0, 100), 'k-', linewidth=0.1)
    #plt.show()
    b, a = signal.butter(4, 10/fnyq, 'low')
    # Plot CST filter
    # TODO investigate why low worN give a weird filter response (check last fav on temp)
    w, h = signal.freqz(b, a, worN=8000)
    plt.figure()
    plt.plot(fnyq*w/np.pi, abs(h))
    plt.title('Filter frequency response')
    plt.xlim([0, 20])
    plt.show()
    CST = signal.lfilter(b, a, spkTrain)

    # Compare signals
    # TODO filtered CST is not right yet (maybe I should be filtering diracs?)
    plt.figure()
    #plt.plot(taux, (np.array(filtSignal)-np.min(filtSignal))/np.max(filtSignal), label='filtered output')
    #plt.plot(taux, (np.array(staticFR)-np.min(staticFR))/np.max(staticFR), label='raw input')
    #plt.plot(taux, (np.array(staticForce)-np.min(staticForce))/np.max(staticForce), label='raw output')
    plt.plot(CST, label='CST')
    plt.legend()
    plt.title(simType)
    plt.xlabel('t (ms)')
    plt.grid()
    plt.show()

    # Performing FFT
    yfo = fft(filtSignal)
    yfo = fftshift(yfo)
    yfi = fft(staticFR)
    yfi = fftshift(yfi)
    cstf = fft(CST)
    cstf = fftshift(cstf)
    ff = fftfreq(N, 1/fs)
    ff = fftshift(ff)
    ffcst = fftfreq(len(cstf), 1/fs)
    ffcst = fftshift(ffcst)

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
    print('******** {} Proportions ********'.format(simType))
    print('*** peak0/peakX')
    print('A0/A1 = {:.2f}'.format(A0/A1))
    print('A0/A2 = {:.2f}'.format(A0/A2))
    print('B0/B1 = {:.2f}'.format(B0/B1))
    print('B0/B2 = {:.2f}'.format(B0/B2))
    print('*** Power of harmonic peaks')
    print('sqrt(A0^2+A1^2+A2^2)/A0 = {:.2f}'.format(
        np.sqrt(A0**2+A1**2+A2**2)/A0))
    print('sqrt(B0^2+B1^2+B2^2)/B0 = {:.2f}'.format(
        np.sqrt(B0**2+B1**2+B2**2)/B0))
    print('*** Power of all peaks')
    indexes = [indexW0, indexW1, indexW2, indexW0n, indexW1n, indexW2n]
    # Remove harmonic peaks
    Bi = [np.abs(x)**2 if y not in indexes else 0.0 for y, x in enumerate(yfo)]
    print('sqrt(B0^2+B1^2+B2^2)/sum(B!=0,1,2) = {:.2f}'.format(
        np.sqrt(B0**2+B1**2+B2**2)/np.sqrt(np.sum(Bi))))

    out[simType] = np.abs(yfo)

    ## Plot FFT for checking whether things are ok
    plt.figure()
    # FFT of output signal TODO should be np.abs(yfo) with ff
    plt.plot(ffcst, np.abs(cstf), 'ko', label='force')
    ## Plot of Bi
    #plt.plot(ff, np.sqrt(Bi), 'bx', label='force w/o main harmonics')
    #plt.vlines(ff, 0, np.abs(yfo))
    # FFT of input signal
    #plt.plot(ff, np.abs(yfi), 'rx', label='input')
    #plt.vlines(ff, 0, np.abs(yfi), color='r', linestyles='dashed')
    plt.title(simType)
    plt.xlabel('f (Hz)')
    plt.ylabel('FFT')
    plt.xlim([0, 10])
    plt.legend()
    plt.grid()
    plt.show()

plt.figure()
plt.plot(ff, out['o'], 'ko', label='Sem CR')
plt.vlines(ff, 0, out['o'], color='k')
plt.plot(ff, out['s'], 'rx', label='Com CR')
plt.vlines(ff, 0, out['s'], color='r')
plt.xlabel('f (Hz)')
plt.ylabel('FFT')
plt.xlim([0, 10])
plt.legend()
plt.grid()
plt.show()
