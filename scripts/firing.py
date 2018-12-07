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
recordedRCIndex = np.random.choice(availableRCs)
amps = [90, 80, 70, 60] #, 50] I decided not to use the last because
                        # it does not bring me anything new and it is easier
                        # to plot without it

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
    for j in range(len(RCSpikeInstants[i])-1):
        instFR[i] = np.append(instFR[i], [1000/(RCSpikeInstants[i][j+1]-RCSpikeInstants[i][j])])
        
    if len(RCSpikeInstants)<1:
        # This occurence cannot be used to calculate instantaneous firing rate
        print ('Occurence of a single spike: Skipped')
        continue
    del RCSpikeInstants[i][0]

# Configuring plot
fig, axes = plt.subplots(nrows=2, ncols=2, sharey=True, sharex=True)

## Add outter axis and turn off axis lines and ticks
outax = fig.add_subplot(111, frameon=False)
outax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
outax.yaxis.labelpad = 15

#import pdb; pdb.set_trace()
for i, ax in enumerate(axes.flatten()):
    #if i==5:
    #    break
    if i==0: # They are shared, only need this once (I suppose)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.set_ylim([0, 1000])
        ax.set_xlim([0, 70])
    ax.plot(RCSpikeInstants[i], instFR[i], 'k.')
    ax.set_title(str(amps[i])+' nA')
outax.set_ylabel('Taxa de disparo instantânea, CR '+str(recordedRCIndex)+' (pps)')
outax.set_xlabel('Tempo (ms)')
#plt.show()
plt.savefig(figsFolder + filenamef + '.svg', format='svg')
