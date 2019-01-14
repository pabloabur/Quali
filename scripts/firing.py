import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.optimize
from matplotlib.ticker import FormatStrFormatter

# File settings
figsFolder = '/home/pablo/git/master-thesis/figuras/'
path = '/home/pablo/osf/Master-Thesis-Data/population/firing/false_decay/'
filenamef = 'firing'
os.chdir(path)

availableRCs = range(1, 601)
recordedRCIndex = 457#np.random.choice(availableRCs)
amps = [18, 12.5, 12.3, 12.1]

# Acquiring data
instFR = [[] for i in range(len(amps))]
RCSpikeInstants = [[] for i in range(len(amps))]
for i, amp in enumerate(amps):
    unitNumber = []
    spikeInstant = []
    
    filename = 'output'+str(i+1)+'.dat'
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        spikeInstant.append(float(line.split()[0]))
        unitNumber.append(int(float(line.split()[1])))
    f.close()
    
    RCSpikeInstants[i] = [y for x, y in enumerate(spikeInstant) if unitNumber[x]==recordedRCIndex]
    if len(RCSpikeInstants[i])<2:
        # This occurence cannot be used to calculate instantaneous firing rate
        print ('Occurence of a single spike or no spike: Skipped')
        RCSpikeInstants[i] = [] # This just ignores the value so it will not throw an error
        continue
    #import pdb; pdb.set_trace()

    for j in range(len(RCSpikeInstants[i])-1):
        instFR[i] = np.append(instFR[i], [1000/(RCSpikeInstants[i][j+1]-RCSpikeInstants[i][j])])
        
    del RCSpikeInstants[i][0]

# Configuring plot
fig, axes = plt.subplots(nrows=2, ncols=2, sharey=True, sharex=True)

## Add outter axis and turn off axis lines and ticks
outax = fig.add_subplot(111, frameon=False)
outax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
outax.yaxis.labelpad = 15

for i, ax in enumerate(axes.flatten()):
    #if i==5:
    #    break
    if i==0: # They are shared, only need this once (I suppose)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.set_ylim([0, 1000])
        ax.set_xlim([0, 100])
    print (RCSpikeInstants[i], instFR[i])
    ax.plot(RCSpikeInstants[i], instFR[i], 'k.')
    ax.set_title('{:0.1f}'.format(amps[i]*100/18) + ' %')
outax.set_ylabel('Taxa de disparo instantânea, CR '+str(recordedRCIndex)+' (pps)')
outax.set_xlabel('Tempo (ms)')
#plt.show()
plt.savefig(figsFolder + filenamef + '.svg', format='svg')

#plt.figure()
#plt.plot(RCSpikeInstants[0], instFR[0], 'k.')
#plt.xlabel('Tempo (ms)')
#plt.ylabel('Taxa de disparo instantânea')
