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
    plt.xlim((0, 110))
    plt.savefig(figsFolder + filenamemod + '.svg', format='svg')

    dx = 0.05
    plt.figure()
    for i in range(3):
        plt.plot(t[0:-1], np.diff(forceOnTrials[i]/dx), symbols[i], label = labels[i])
    plt.legend()
    plt.ylabel('Derivada da força (N/s)')
    plt.xlabel('Tempo (ms)')
    plt.xlim((0, 35))
    plt.savefig(figsFolder + filenameder + '.svg', format='svg')
    #plt.show()

def lowInput(dataPath):
    tmin = 500
    nTrials = 5
    # Files and paths
    filenamestats = 'res_stat'
    figsFolder = '/home/pablo/git/master-thesis/figuras/'

    #****************************************
    #******* Getting and processing high input data
    #****************************************
    meanCoeffVar = {'Forte': [], 'Normal': [], 'Fraco': []}
    for nTrial in range(1, nTrials+1):
        files = glob.glob(dataPath + '/trial' + str(nTrial) + '/forcelo*.dat')
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

            staticForce = [y for x,y in enumerate(force) if t[x]>tmin]
            
            forceOnTrials[i] = np.array(force)

            if filename[-5] == 'd':
                labels.append('Forte')
                coeffVar = np.std(staticForce)/np.mean(staticForce)*100
                meanCoeffVar['Forte'].append(coeffVar)
            elif filename[-5] == 's':
                labels.append('Normal')
                coeffVar = np.std(staticForce)/np.mean(staticForce)*100
                meanCoeffVar['Normal'].append(coeffVar)
            elif filename[-5] == 'h':
                labels.append('Fraco')
                coeffVar = np.std(staticForce)/np.mean(staticForce)*100
                meanCoeffVar['Fraco'].append(coeffVar)

        #plt.figure()
        #symbols = ['k', 'k--', 'k:']
        #for i in range(3):
        #    plt.plot(t, forceOnTrials[i], symbols[i], label = labels[i])
        #plt.legend()
        #plt.ylabel('Força (N)')
        #plt.xlabel('Tempo (ms)')
        #plt.show()

    for key, value in meanCoeffVar.items():
        print('mean CV of force:{:.2f}, {}'.format(np.mean(value), key))
        print('sd CV of force:{:.2f}, {}'.format(np.std(value), key))

    print(meanCoeffVar)
    plt.figure()
    for i, j in enumerate(meanCoeffVar):
        plt.plot([i+1]*nTrials, meanCoeffVar[j], 'ko')
    #import pdb; pdb.set_trace()
    plt.xticks(range(1, len(meanCoeffVar)+1), list(meanCoeffVar.keys()))
    plt.ylabel('Coeficiente de variação')
    plt.xlabel('Força da inibição recorrente (ms)')
    plt.show()
    #plt.savefig(figsFolder + filenamestats + '.svg', format='svg')

#trial = input('High input trial number: ')
#sub_trial = input('High input subtrial number: ')
#dataPath = ('/home/pablo/osf/Master-Thesis-Data/population/modulation'
#            '/high/trial' + str(trial) + '/trial' + str(sub_trial))
#
#highInput(dataPath)

trial = input('Low input trial number: ')
dataPath = ('/home/pablo/osf/Master-Thesis-Data/population/modulation'
            '/low/trial' + str(trial))

lowInput(dataPath)
