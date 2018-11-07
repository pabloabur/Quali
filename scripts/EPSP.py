import matplotlib.pyplot as plt
import numpy as np

# File settings
figsFolder = '/home/pablo/git/master-thesis/figuras/'
filenamePath = '/home/pablo/osf/Master-Thesis-Data/cell/EPSP/EPSP.dat'
filename = 'EPSP'

t = []
RCV = []
f = open(filenamePath, 'r')
lines = f.readlines()
for line in lines:
    t.append(float(line.split()[0]))
    RCV.append(float(line.split()[1]))
f.close()

maxPosition = [x for x, y in enumerate(RCV) if y==max(RCV)][0]

plt.figure()
plt.plot(t, RCV)
plt.xlabel('tempo (ms)')
plt.ylabel('Potencial de membrana (mV)')
plt.axvline(x=t[maxPosition], color='r', label='Pico em t='+str(t[maxPosition])+' ms')
plt.grid(True)
plt.xlim([5, 70])
plt.legend()
#plt.show()
plt.savefig(figsFolder + filename + '.svg', format='svg')
