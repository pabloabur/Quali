import matplotlib.pyplot as plt
import numpy as np
import glob
import os
from scipy.interpolate import UnivariateSpline

# File settings
figsFolder = '/home/pablo/git/master-thesis/figuras/'
path = '/home/pablo/osf/Master-Thesis-Data/population/McHamm/false_decay/trial4/'
filenameWidth = 'mchammwidth'
filenameAmplitude = 'mchammamplitude'
filenameRise = 'mchammrise'
filenameDecay = 'mchammdecay'
os.chdir(path)

simDuration_ms = 50
timeStep_ms = 0.05
t = np.arange(0, simDuration_ms, timeStep_ms)
nMN = 300
cutoff_value = 1.0
chosenMN = 173 # This came from .dat generated, but I subtracted by one

boundary = 4.7
RIPSPs = []
distances = []
positions = []
recordedMN = []
MNsignal = np.zeros((len(t), nMN))
files=glob.glob('*.dat') # Responsable for getting only MNV files
positionsFile = 'positions.dat'
files.remove(positionsFile)

f = open(positionsFile, 'r')
lines = f.readlines()
for line in lines:
    positions.append(float(line.split()[0]))
f.close()

# Preparing subplot for Hamm amplitudes
fig, ax = plt.subplots(nrows=3, ncols=5)
ax = ax.flatten()
fig.tight_layout()

for filenumber, filename in enumerate(files):
    # Opening MN signal in each file
    f = open(filename, 'r')
    lines = f.readlines()
    for i, line in enumerate(lines):
        MNsignal[i,:] = np.array([float(x) for x in line.split()])
    f.close()

    # Retrieving useful information
    peaks = [min(MNsignal[:,x]) for x in range(MNsignal.shape[1])]
    stimulatedMNIndex = int(filename[3:6])-1 # -1 because array starts in 0 in Python
    availableMNsIndex = [x for x in range(nMN)]
    del availableMNsIndex[stimulatedMNIndex]

    # Hamm amplitude plots
    #import pdb; pdb.set_trace()
    absPeaks = [1000*abs(y) for x,y in enumerate(peaks) if x!=stimulatedMNIndex]
    binsamp = np.linspace(min(absPeaks),max(absPeaks),len(absPeaks)/20)
    ax[filenumber].plot(3, 5, filenumber+1)
    ax[filenumber].hist(absPeaks, bins=binsamp, color='k')
    ax[filenumber].set_title(str(stimulatedMNIndex))

    # Chosen by hand
    if chosenMN==stimulatedMNIndex:
        # Calculate rise time
        riseTime = []
        for i in range(MNsignal.shape[1]):
            if i==stimulatedMNIndex:
                continue
            for j in range(MNsignal.shape[0]):
                if MNsignal[j,i]!=0.0:
                    ti = j
                    tf = np.where(MNsignal[:,i]==peaks[i])[0][0]
                    riseTime.append(t[tf]-t[ti])
                    break
    
        binsrise = np.linspace(min(riseTime),max(riseTime),len(riseTime)/30)

        # Calculate half-width
        half_width = []
        for i in range(MNsignal.shape[1]):
            if i == stimulatedMNIndex:
                continue
            if min(MNsignal[:,i]) == 0:
                print ('Warning: minimum value of a MN signal equals zero')
                continue
            spline = UnivariateSpline(t, MNsignal[:,i] - min(MNsignal[:,i])/2, s=0)
            roots = spline.roots()
            if len(roots)>2:
            # This can be caused by very small RIPSPs that generate staircase
            # like responses. Generally, they are two groups of close values,
            # so taking the first and the last is good enough to calculate
            # half-width. This should be constantly checked, though, as I 
            # am not sure it is always like this
                print ('Warning: Irregular RIPSP caused more than two roots at index '+str(i))
                r1 = roots[0]
                r2 = roots[-1]
            elif len(roots)<2:
                print ('Warning: Only one root at index '+str(i))
                continue
            else:
                r1, r2 = roots
            half_width.append(r2-r1)
            
        binswidth = np.linspace(min(half_width),max(half_width),len(half_width)/20)

    # Iterating over each chosen MN to get topographic recordings
    recordedCount = 0
    while recordedCount < 13:
	# Random choice to get approximately 180 pairs (14*13=182)
        MNCandidateIndex = np.random.choice(availableMNsIndex)
        distance = positions[MNCandidateIndex] - positions[stimulatedMNIndex]
        # Ignore recordings out of the boundary or repeated recordings
        if abs(distance)>boundary or MNCandidateIndex in recordedMN:
            continue
        recordedMN.append(MNCandidateIndex)
        distances.append(distance)
        RIPSPs.append(1000*peaks[MNCandidateIndex])
        recordedCount+=1

# Ploting results
# Closing and showing Hamm plots
ax[-1].axis('off')
ax[-2].axis('off')
plt.savefig(figsFolder + filenameAmplitude + '.svg', format='svg')
#plt.show()

plt.figure()
plt.plot(distances, RIPSPs, 'k.')
plt.xlabel('Distância entre MNs (mm)')
plt.ylabel('Amplitudes dos PIPS recorrentes ($\mu$V)')
plt.savefig(figsFolder + filenameDecay + '.svg', format='svg')
#plt.show()

plt.figure()
plt.hist(riseTime, bins=binsrise, color='k')
plt.ylabel('Quantidades observadas')
plt.xlabel('Tempo de subida (ms)')
plt.savefig(figsFolder + filenameRise + '.svg', format='svg')
#plt.show()

plt.figure()
plt.hist(half_width, bins=binswidth, color='k')
plt.ylabel('Quantidades observadas')
plt.xlabel('Tempo de meia vida (ms)')
plt.savefig(figsFolder + filenameWidth + '.svg', format='svg')
#plt.show()

# Calculating mean among close and distant MNs
closeidx = [x for x in range(len(distances)) if abs(distances[x])<=cutoff_value]
close_pairs = [RIPSPs[x] for x in closeidx if RIPSPs[x] != 0.0]
distantidx = [x for x in range(len(distances)) if abs(distances[x])>cutoff_value]
distant_pairs = [RIPSPs[x] for x in distantidx if RIPSPs[x] != 0.0]
RIPSP_close = np.mean(close_pairs)
RIPSP_distant = np.mean(distant_pairs)

print ('Number of close pairs: '+str(len(close_pairs)))
print ('Number of distant pairs: '+str(len(distant_pairs)))
print ('Mean RIPSP in close pairs (micro Volts): '+str(RIPSP_close))
print ('Mean RIPSP in distant pairs (micro Volts): '+str(RIPSP_distant))
