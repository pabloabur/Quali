import matplotlib.pyplot as plt
import numpy as np

# File settings
figsFolder = '/home/pablo/git/master-thesis/figuras/'
filenamePath = '/home/pablo/osf/Master-Thesis-Data/cell/FxI/FxI.dat'
filenamePathRC = '/home/pablo/osf/Master-Thesis-Data/cell/FxI/FxI_RC.dat'
filename = 'FxI'
filenameRC = 'FxI_RC'

I = []
F1 = []
F2 = []
F3 = []
F4 = []
t = []
RC = []
f = open(filenamePath, 'r')
lines = f.readlines()
for line in lines:
    I.append(float(line.split()[0]))
    F1.append(float(line.split()[1]))
    F2.append(float(line.split()[2]))
    F3.append(float(line.split()[3]))
    F4.append(float(line.split()[4]))
f.close()

f = open(filenamePathRC, 'r')
lines = f.readlines()
for line in lines:
    t.append(float(line.split()[0]))
    RC.append(float(line.split()[1]))
f.close()

plt.figure()
plt.plot(I, F1, 'k', label='Primeiro intervalo')
plt.plot(I, F2, label='Segundo intervalo')
plt.plot(I, F3, label='Terceiro intervalo')
plt.plot(I, F4, label='Regime estacionário')
plt.xlabel('Intensidade de corrente injetada (nA)')
plt.ylabel('Frequência de disparo (pps)')
plt.legend()
plt.grid(True)
#plt.show()
plt.savefig(figsFolder + filename + '.svg', format='svg')

plt.figure()
plt.plot(t, RC, 'k')
plt.xlabel('tempo (ms)')
plt.ylabel('Potencial de membrana (mV)')
#plt.show()
plt.savefig(figsFolder + filenameRC + '.svg', format='svg')
