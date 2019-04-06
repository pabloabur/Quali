import numpy as np
import matplotlib.pyplot as plt
import glob

def maxInput(dataPath, trial):
    # Files and paths
    filenamemod = 'res_moda'
    filenameder = 'res_modb'
    figsFolder = '/home/pablo/git/master-thesis/figuras/'

    #****************************************
    #******* Getting and processing high input data
    #****************************************
    simTypes = ['o', 'h', 's', 'd']
    nMod = len(simTypes)
    forceOnTrials = {'d': [], 's': [], 'h': [], 'o': []}
    labels = {'d': 'Forte', 's': 'Normal', 'h': 'Fraco', 'o': 'Ausente'}
    symbols = {'d': 'k', 's': 'k--', 'h': 'k-.', 'o': 'k:'}
    for simType in simTypes:
        force = []
        t = []
        
        fileName = dataPath + '/max/trial' + str(trial) + '/force' + simType + '.dat'
        try:
            f = open(fileName, 'r')
        except:
            print('Warning: File ' + fileName + ' could not be opened.')
            continue
        lines = f.readlines()
        for line in lines:
            t.append(float(line.split()[0]))
            force.append(float(line.split()[1]))
        f.close()
        
        forceOnTrials[simType] = np.array(force)
        staticForce = [y for x,y in enumerate(forceOnTrials[simType]) if t[x]>200]
        var = np.var(staticForce)
        ave = np.mean(staticForce)
        labels[simType] = labels[simType] + str(ave)

    plt.figure()
    for simType in simTypes:
        plt.plot(t, forceOnTrials[simType], symbols[simType], label = labels[simType])
    plt.legend()
    plt.ylabel('Força (N)')
    plt.xlabel('Tempo (ms)')
    plt.xlim((0, 110))
    # TODO save only
    #plt.savefig(figsFolder + filenamemod + '.svg', format='svg')

    dx = 0.05
    plt.figure()
    for simType in simTypes:
        plt.plot(t[0:-1], np.diff(forceOnTrials[simType]/dx), symbols[simType], label = labels[simType])
    plt.legend()
    plt.ylabel('Derivada da força (N/s)')
    plt.xlabel('Tempo (ms)')
    plt.xlim((0, 35))
    # TODO save only
    #plt.savefig(figsFolder + filenameder + '.svg', format='svg')
    plt.show()

def constInput(dataPath, option, nTrials):
    tmin = 500
    # Files and paths
    filenamestats = 'res_stat'
    figsFolder = '/home/pablo/git/master-thesis/figuras/'
    if option == 'low':
        datFile = '/force*.dat'
        dataPath = dataPath + '/low/'
    else:
        datFile = '/force*.dat'
        dataPath = dataPath + '/high/'

    #****************************************
    #******* Getting and processing input data
    #****************************************
    meanCoeffVar = {'Forte': [], 'Normal': [], 'Fraco': [], 'Ausente': []}
    nMod = len(meanCoeffVar)
    for nTrial in range(1, nTrials+1):
        #*****************************
        #*********** Spikes plot
        #*****************************
        # TODO save this image for discussion
        #spikeTimes = []
        #spikeUnits = []
        #fileName = dataPath + 'trial' + str(nTrial) + '/spikeo.dat'
        #f = open(fileName, 'r')
        #lines = f.readlines()
        #for line in lines:
        #    spikeTimes.append(float(line.split()[0]))
        #    spikeUnits.append(float(line.split()[1]))
        #f.close()

        #fig, ax = plt.subplots(1)
        #plt.plot(spikeTimes, spikeUnits, '.')
        ##ax.plot((spikeTimes, spikeTimes), (0, 100), 'k-', linewidth=0.1)
        #plt.xlabel('Tempo (ms)')
        #plt.ylabel('Índices dos MNs')
        #plt.title('open')
        #plt.xlim([1750, 2000])

        #spikeTimes = []
        #spikeUnits = []
        #fileName = dataPath + 'trial' + str(nTrial) + '/spiked.dat'
        #f = open(fileName, 'r')
        #lines = f.readlines()
        #for line in lines:
        #    spikeTimes.append(float(line.split()[0]))
        #    spikeUnits.append(float(line.split()[1]))
        #f.close()

        #fig, ax = plt.subplots(1)
        #plt.plot(spikeTimes, spikeUnits, '.')
        ##ax.plot((spikeTimes, spikeTimes), (0, 100), 'k-', linewidth=0.1)
        #plt.xlabel('Tempo (ms)')
        #plt.ylabel('Índices dos MNs')
        #plt.title('double')
        #plt.xlim([1750, 2000])
        #plt.show()

        files = glob.glob(dataPath + 'trial' + str(nTrial) + datFile)
        forceOnTrials = [[] for _ in range(nMod)]
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
            var = np.var(staticForce)
            ave = np.mean(staticForce)
            
            #import pdb; pdb.set_trace()
            forceOnTrials[i] = np.array(force)

            if filename[-5] == 'd':
                labels.append('Forte'+str(ave))
                coeffVar = np.std(staticForce)/np.mean(staticForce)*100
                meanCoeffVar['Forte'].append(coeffVar)
            elif filename[-5] == 's':
                labels.append('Normal'+str(ave))
                coeffVar = np.std(staticForce)/np.mean(staticForce)*100
                meanCoeffVar['Normal'].append(coeffVar)
            elif filename[-5] == 'h':
                labels.append('Fraco'+str(ave))
                coeffVar = np.std(staticForce)/np.mean(staticForce)*100
                meanCoeffVar['Fraco'].append(coeffVar)
            elif filename[-5] == 'o':
                labels.append('Ausente'+str(ave))
                coeffVar = np.std(staticForce)/np.mean(staticForce)*100
                meanCoeffVar['Ausente'].append(coeffVar)

        ## Plot forces
        # TODO comment this
        plt.figure()
        symbols = ['k', 'k--', 'k:', 'k-.']
        for i in range(nMod):
            plt.plot(t, forceOnTrials[i], symbols[i], label = labels[i])
        plt.legend()
        plt.ylabel('Força (N)')
        plt.xlabel('Tempo (ms)')
        plt.show()

    for key, value in meanCoeffVar.items():
        print('mean CV of force:{:.2f}, {}'.format(np.mean(value), key))
        print('sd CV of force:{:.2f}, {}'.format(np.std(value), key))

    meanSync = {'Forte': [], 'Normal': [], 'Fraco': [], 'Ausente': []}
    for nTrial in range(1, nTrials+1):
        files = glob.glob(dataPath + 'trial' + str(nTrial) + '/sync*.dat')
        syncs = [[] for _ in range(nMod)]
        syncLabels = []
        # Iterate over modulations within a trial
        for i, filename in enumerate(files):
            sync = []
            
            f = open(filename, 'r')
            lines = f.readlines()
            for line in lines:
                sync.append(float(line.split()[0]))
            f.close()

            if filename[-5] == 'd':
                syncLabels.append('Forte')
                meanSync['Forte'].extend(sync)
            elif filename[-5] == 's':
                syncLabels.append('Normal')
                meanSync['Normal'].extend(sync)
            elif filename[-5] == 'h':
                syncLabels.append('Fraco')
                meanSync['Fraco'].extend(sync)
            elif filename[-5] == 'o':
                syncLabels.append('Ausente')
                meanSync['Ausente'].extend(sync)

    # Plot coefficients
    fig, ax = plt.subplots(2, 1, sharex=True)
    ticks = []
    for i, j in enumerate(meanSync):
        ticks.append(j)
        ax[0].plot([i+1]*nTrials, meanSync[j], 'ko', fillstyle='none')
    for i, j in enumerate(meanCoeffVar):
        if ticks[i] != j:
            print('Potential danger')
        ax[1].plot([i+1]*nTrials, meanCoeffVar[j], 'ko', fillstyle='none')
    plt.xticks(range(1, len(meanSync)+1), list(meanSync.keys()))
    ax[0].set(ylabel='Coeficiente de sincronia')
    ax[1].set(xlabel='Força da inibição recorrente', ylabel='Coeficiente de variação')
    # TODO save only
    plt.show()
    #plt.savefig(figsFolder + filenamestats + '.svg', format='svg')

dataPath = ('/home/pablo/osf/Master-Thesis-Data/population/modulation')
numTrials = 5
# For the initial instants, result does not change so just pick one trial 
# for max simulation
chosenTrial = 5

maxInput(dataPath, chosenTrial)
constInput(dataPath, 'low', numTrials)
constInput(dataPath, 'high', numTrials)
