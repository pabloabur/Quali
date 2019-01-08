import matplotlib.pyplot as plt
import numpy as np

# File settings
figsFolder = '/home/pablo/git/master-thesis/figuras/'
filenamePath = '/home/pablo/osf/Master-Thesis-Data/cell/IPSP/IPSP.dat'
filename = 'IPSP'

t = []
S = []
FR = []
FF = []
f = open(filenamePath, 'r')
lines = f.readlines()
for line in lines:
    t.append(float(line.split()[0]))
    # units from Fortran are in mV, so 1e3 multiplied is required
    # to convert to \muV
    S.append(1000*float(line.split()[1]))
    FR.append(1000*float(line.split()[2]))
    FF.append(1000*float(line.split()[3]))
f.close()

#print (str(min(S)))
#print (str(min(FR)))
#print (str(min(FF)))
plt.figure()
plt.plot(t, S, 'k', label='Motoneurônio do tipo S')
plt.plot(t, FR, label='Motoneurônio do tipo FR')
plt.plot(t, FF, label='Motoneurônio do tipo FF')
plt.legend()
plt.xlabel('tempo (ms)')
plt.ylabel('Potencial de membrana ($\mu$V)')
plt.grid(True)
#plt.show()
plt.savefig(figsFolder + filename + '.svg', format='svg')
