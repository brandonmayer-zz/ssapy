from ssapy import agentFactory, timestamp_
from ssapy.pricePrediction.jointGMM import jointGMM, expectedSurplus

from ssapy.strategies.jointLocal import jointLocal
from ssapy.strategies.margLocal import margLocal

import pickle
import os

def compareMargJointLocal(rootDir = None, scppFile = None, nItr = 10000, n_expectedSurplus_samples = 10000):
    if rootDir == None:
        raise ValueError("Must specify output directory - oDir")
    
    if scppFile == None:
        raise ValueError("Must specify scpp file (pkl)")
    
    rootDir = os.path.realpath(rootDir)
    
    
    oDir = os.path.join(rootDir, "compareMargLocal_{0}".format(timestamp_()))
    if not os.path.exists(oDir):
        os.makedirs(oDir)
        
        
    for itr in xrange(nItr):
        pass
        
    

def main():
    pass

if __name__ == "__main__":
    main()