from collections import OrderedDict

def ensembleFR(spikeInstant, unitNumber, transientPeriod, simDuration):
    units = list(OrderedDict.fromkeys(unitNumber)) # Getting non repeated values
    #import pdb; pdb.set_trace()
    
    if len(units) == 0:
        return 0
    else:
        meanFR = []
        for unit in units:
            MNSpikeInstants = [y for x, y in enumerate(spikeInstant) if
                    unitNumber[x]==unit]
            numberOfSpikes = len([x for x in MNSpikeInstants if
                x>transientPeriod])
            # Ignoring cases in which motoneuron did not fire
            if numberOfSpikes == 0:
                continue
            meanFR.append(numberOfSpikes/(simDuration*1e-3 -
                transientPeriod*1e-3))

    #     popSlice = [y for x, y in enumerate(meanFR) if x>100 and x<200]
    #     sliceFR = sum(popSlice)/(len(popSlice))
    #     FR = sum(meanFR)/len(meanFR)

    #     plt.figure()
    #     plt.plot(units, meanFR, 'o')
    #     plt.axhline(y=FR, color='r', linestyle='-')
    #     plt.axhline(y=sliceFR, color='k', linestyle='-')
    #     plt.show()

        return sum(meanFR)/len(units)
