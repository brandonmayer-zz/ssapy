from auctionSimulator.hw4.auctions.simultaneousAuction import *
from auctionSimulator.parallelWorker import *

import numpy
import matplotlib.pyplot as plt
import time
import itertools
import multiprocessing
import os

def drange(start,stop,step):
        r = start
        while r <= stop:
            yield r
            r += step
            
def main():
    aStart = -20
    aStop = 0
    aStep = 1
    
    nGames = 1000
    
    NUM_PROC = 11
    
    margDistPkl = "C:\\bmProjects\\courses\\fall2011\\csci2951\\" +\
                  "auctionSimulator\\hw4\\pricePrediction\\margDistPredictions\\" +\
                  "distPricePrediction_straightMU8_10000_2011_12_8_1323383753.pkl"
                  
    outDir = "F:\\courses\\fall2011\\csci2951\\hw4\\exp7\\"
    
    
                  
    margDistPrediction = margDistSCPP()
    
    margDistPrediction.loadPickle(margDistPkl)
    
#    margDistPrediction.graphPdf()
    agentNames = []
    agentNames.append('riskAwareTMUS8')
    agentNames.append('targetMUS8')
    agentNames.append('targetMUS8')
    agentNames.append('targetMUS8')
    agentNames.append('targetMUS8')
    agentNames.append('targetMUS8')
    agentNames.append('targetMUS8')
    agentNames.append('targetMUS8')
    
    parallel = True
    
    writeTxt = False
       
    results = []
    keys = []
    for A in drange(aStart,aStop,aStep):
        
        pw = parallelSimAuctionSymmetricVL( margDistPrediction = margDistPrediction,
                                            agentList          = agentNames,
                                            m                  = 5,
                                            nGames             = nGames,
                                            A                  = A)
        
        print 'Computing Result for A = {0}'.format(A)
        
        
        
        start = time.clock()
        if parallel:
            pool = multiprocessing.Pool(processes = NUM_PROC)
            result = numpy.atleast_2d( pool.map(pw,xrange(0,NUM_PROC)) ).astype(numpy.float)
            pool.close()
            pool.join()
        else:
            result = numpy.atleast_2d([r for r in itertools.imap(pw,xrange(0,NUM_PROC))]).astype(numpy.float)
        finish = time.clock()
        
        print 'Finished {0} games in {1}'.format(nGames*NUM_PROC,finish-start)
        
        result = numpy.reshape( result,(result.shape[0]*result.shape[1],result.shape[2]) )
        
        if writeTxt:
            textFile = outDir + "result_A_{0}.txt".format(A)
            
            numpy.savetxt(textFile,result)
        
        keys.append(A)
        
        results.append(result)
        
    outFileZ = outDir + "results_A_{0}_{1}_{2}_nGames_{3}".format(aStart,aStop,aStep,nGames*NUM_PROC)
    numpy.savez(outFileZ,results = numpy.dstack(results), A = keys, nGames = nGames*NUM_PROC)    
    
    print 'Finished.'

if __name__ == "__main__":
    main()