import numpy as np
import matplotlib.pyplot as plt
import glob

def highInput(dataPath):
    # Files and paths
    filenamemod = 'res_moda'
    filenameder = 'res_modb'
    figsFolder = '/home/pablo/git/master-thesis/figuras/'

    #****************************************
    #******* Getting and processing high input data
    #****************************************
    files = glob.glob(dataPath + '/forcehi*.dat')
    forceOnTrials = [[] for _ in range(3)]
    labels = []
    for i, filename in enumerate(files):
        force = []
        t = []
        
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            t.append(float(line.split()[0]))
            force.append(float(line.split()[1]))
        f.close()
        
        #import pdb; pdb.set_trace()
        forceOnTrials[i] = np.array(force)
        if filename[-5] == 'd':
            labels.append('Forte')
        elif filename[-5] == 's':
            labels.append('Normal')
        elif filename[-5] == 'h':
            labels.append('Fraco')

    plt.figure()
    symbols = ['k', 'k--', 'k:']
    for i in range(3):
        plt.plot(t, forceOnTrials[i], symbols[i], label = labels[i])
    plt.legend()
    plt.ylabel('Força (N)')
    plt.xlabel('Tempo (ms)')
    plt.savefig(figsFolder + filenamemod + '.svg', format='svg')
    #plt.show()

    dx = 0.05
    plt.figure()
    for i in range(3):
        plt.plot(t[0:-1], np.diff(forceOnTrials[i]/dx), symbols[i], label = labels[i])
    plt.legend()
    plt.ylabel('Derivada da força (N)')
    plt.xlabel('Tempo (ms)')
    plt.savefig(figsFolder + filenameder + '.svg', format='svg')
    #plt.show()

lowInput(dataPath):
    # Files and paths
    filenamestats = 'res_stat'
    figsFolder = '/home/pablo/git/master-thesis/figuras/'

    #****************************************
    #******* Getting and processing high input data
    #****************************************
    files = glob.glob(dataPath + '/forcelo*.dat')
    forceOnTrials = [[] for _ in range(3)]
    labels = []
    for i, filename in enumerate(files):
        force = []
        t = []
        
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            t.append(float(line.split()[0]))
            force.append(float(line.split()[1]))
        f.close()
        
        #import pdb; pdb.set_trace()
        forceOnTrials[i] = np.array(force)
        if filename[-5] == 'd':
            labels.append('Forte')
        elif filename[-5] == 's':
            labels.append('Normal')
        elif filename[-5] == 'h':
            labels.append('Fraco')

    plt.figure()
    symbols = ['k', 'k--', 'k:']
    for i in range(3):
        plt.plot(t, forceOnTrials[i], symbols[i], label = labels[i])
    plt.legend()
    plt.ylabel('Força (N)')
    plt.xlabel('Tempo (ms)')
    plt.savefig(figsFolder + filenamestats + '.svg', format='svg')
    #plt.show()

trial = input('High input trial number: ')
dataPath = ('/home/pablo/osf/Master-Thesis-Data/population/modulation'
            '/high/trial' + str(trial))

highInput(dataPath)

trial = input('Low input trial number: ')
dataPath = ('/home/pablo/osf/Master-Thesis-Data/population/modulation'
            '/low/trial' + str(trial))

lowInput(dataPath)
