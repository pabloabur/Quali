import matplotlib.pyplot as plt
import numpy as np

# File settings
figsFolder = '/home/pablo/git/master-thesis/figuras/'
filenamePath = '/home/pablo/osf/Master-Thesis-Data/cell/AHP/AHP.dat'
filename = 'AHP'

t = []
RCV = []
f = open(filenamePath, 'r')
lines = f.readlines()
for line in lines:
    t.append(float(line.split()[0]))
    RCV.append(float(line.split()[1]))
f.close()

plt.figure()
plt.plot(t, RCV)
plt.xlabel('tempo (ms)')
plt.ylabel('Potencial de membrana (mV)')
plt.grid(True)
plt.xlim([0, 60])
plt.ylim([-5, 10])
#plt.show()
plt.savefig(figsFolder + filename + '.svg', format='svg')
