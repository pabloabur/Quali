import matplotlib.pyplot as plt
import numpy as np

t = []
RCV = []
figsFolder = '/home/pablo/git/master-thesis/figuras/'

filename = '/home/pablo/osf/Master-Thesis-Data/AHP/RCSpikes.dat'
f = open(filename, 'r')
lines = f.readlines()
for line in lines:
    t.append(float(line.split()[0]))
    RCV.append(float(line.split()[1]))
f.close()

plt.figure()
plt.plot(t, RCV)
plt.xlabel('t (ms)')
plt.ylabel('V (mV)')
plt.grid(True)
plt.xlim([0, 60])
plt.ylim([-5, 10])
plt.show()
plt.savefig(figsFolder + 'AHP.svg', format='svg')
