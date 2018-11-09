import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# File settings
figsFolder = '/home/pablo/git/master-thesis/figuras/'
path = '/home/pablo/osf/Master-Thesis-Data/population/McHamm/false_decay/trial1/'
filename = 'McHamm'
os.chdir(path)

simDuration_ms = 50
timeStep_ms = 0.05
t = np.arange(0, simDuration_ms, timeStep_ms)
nMN = 300

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

for fil in files:
    f = open(fil, 'r')
    lines = f.readlines()
    for i, line in enumerate(lines):
        MNsignal[i,:] = np.array([float(x) for x in line.split()])
    f.close()

    peaks = [min(MNsignal[:,x]) for x in range(MNsignal.shape[1])]
    stimulatedMNIndex = int(fil[3:6])-1 # -1 because array starts in 0 in Python
    availableMNsIndex = [x for x in range(nMN)]
    del availableMNsIndex[stimulatedMNIndex]
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
        RIPSPs.append(peaks[MNCandidateIndex])
        recordedCount+=1

plt.figure()
plt.plot(distances, RIPSPs, '.')
plt.title('Topographic RIPSP')
plt.xlabel('mm')
plt.ylabel('mV')
plt.show()

cutoff_value = 1.4

closeidx = [x for x in range(len(distances)) if abs(distances[x])<=cutoff_value]
close_pairs = [RIPSPs[x] for x in closeidx if RIPSPs[x] != 0.0]
distantidx = [x for x in range(len(distances)) if abs(distances[x])>cutoff_value]
distant_pairs = [RIPSPs[x] for x in distantidx if RIPSPs[x] != 0.0]
RIPSP_close = np.mean(close_pairs)
RIPSP_distant = np.mean(distant_pairs)

print ('Mean RIPSP in close pairs (micro Volts): '+str(RIPSP_close*1e3))
print ('Mean RIPSP in distant pairs (micro Volts): '+str(RIPSP_distant*1e3))
