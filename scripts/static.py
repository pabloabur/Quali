import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import scipy.optimize

# File settings
figsFolder = '/home/pablo/git/master-thesis/figuras/'
path = '/home/pablo/osf/Master-Thesis-Data/population/Static/false_decay/trial1/'
filename24 = 'static24'
filenamenorm = 'staticnorm'
os.chdir(path)

tmin = 500
simDuration_ms = 1000
availableRCs = range(1, 601)
recordedRCs = np.random.choice(availableRCs, size=24, replace=False)
print ('Recorded RCs #' + str(recordedRCs))
freqs = [x for x in range(10, 80, 10)]
firingRates = [[0]*len(freqs) for i in range(len(recordedRCs))]

def langmuir(f, c, k):
    return c*f/(k + f)

for i, recordedRC in enumerate(recordedRCs):
    for j, freq in enumerate(freqs):
        unitNumber = []
        spikeInstant = []
        filename = 'output'+str(freq)+'.dat'
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            spikeInstant.append(float(line.split()[0]))
            unitNumber.append(int(float(line.split()[1])))

        RCSpikeInstants = [y for x, y in enumerate(spikeInstant) if unitNumber[x]==recordedRC]
        numberOfSpikes = len([x for x in RCSpikeInstants if x>tmin])
        firingRates[i][j] = float(numberOfSpikes)*1e3/(simDuration_ms-tmin)

cs = []
plt.figure()
for firingRate in firingRates:
    # Curve fitting
    try:
        # maxfev is passed to least method square and avoids runtime error
        fit_params, pcov = scipy.optimize.curve_fit(langmuir, freqs,
                firingRate, bounds=(0, np.inf), maxfev=2000)
        cs.append(fit_params[0])
    except RuntimeError:
        print ('Least square method failed. The value was ignored')
        
    fittedLangmuir = langmuir(np.linspace(0, 70, 100), *fit_params)
    plt.plot(np.linspace(0, 70, 100), fittedLangmuir)
plt.xlabel('Frequência do estímulo antidrômico (Hz)')
plt.ylabel('Taxa de disparo da CR (pps)')
plt.savefig(figsFolder + filename24 + '.svg', format='svg')
#plt.show()

# Langmuir curves averaging
npRates = np.array(firingRates)

# Normalization
for i, c in enumerate(cs):
    npRates[i,:] = npRates[i,:]/c
    
# Statistics
numbCurves = npRates.shape[0]
aveRate = np.sum(npRates, axis=0)/numbCurves
stdRate = np.std(npRates, axis=0)

fit_params, pcov = scipy.optimize.curve_fit(langmuir, freqs, aveRate, bounds=(0, np.inf), maxfev=2000)
aveLangmuir = langmuir(np.linspace(0, 70, 100), *fit_params)

# Plots
plt.figure()
plt.errorbar(freqs, aveRate, stdRate, linestyle='None', marker='o', color='k')
plt.plot(np.linspace(0, 70, 100), aveLangmuir, 'k', label='Langmuir fitted to mean')
plt.ylim([0, 1])
plt.xlabel('Frequência do estímulo antidrômico (Hz)')
plt.ylabel('Taxa média de disparo da CR normalizada (pps)')
plt.savefig(figsFolder + filenamenorm + '.svg', format='svg')
#plt.show()
