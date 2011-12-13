from auctionSimulator.hw4.auctions.simultaneousAuction import *
from auctionSimulator.parallelWorker import *

import numpy
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
    aStart = 0
    aStop = 8
    aStep = 1
    
    nGamesPerCore = 1000
    NUM_PROC = multiprocessing.cpu_count() - 1
    nGamesTot = nGamesPerCore*NUM_PROC
    
    margDistPkl = "C:\\bmProjects\\courses\\fall2011\\csci2951\\" +\
                  "auctionSimulator\\hw4\\pricePrediction\\margDistPredictions\\" +\
                  "distPricePrediction_straightMU8_10000_2011_12_8_1323383753.pkl"
                  
    margDistPrediction = margDistSCPP()
    
    margDistPrediction.loadPickle(margDistPkl)
                  
    outDir = "F:\\courses\\fall2011\\csci2951\\hw4\\exp8\\"
    if not os.path.isdir(outDir):
        os.makedirs(outDir)
    
    
    parallel = True
    
    agentTypeList = []
    agentTypeList.append('riskAwareTMUS8')
    agentTypeList.append('targetMUS8')
    agentTypeList.append('targetMU8')
    agentTypeList.append('straightMU8')
    agentTypeList.append('bidEvaluatorSMU8')
    agentTypeList.append('bidEvaluatorTMUS8')

    keys = []
    results = []
    for A in drange(aStart,aStop,aStep):
        
        print 'Running Simulation for A = {0}'.format(A)
        
        pw = parallelSimAuctionSymmetricVL( margDistPrediction = margDistPrediction,
                                            agentList          = agentTypeList,
                                            m                  = 5,
                                            nGames             = nGamesPerCore,
                                            A                  = A)
        
        
        start = time.clock()
        if parallel:
            pool = multiprocessing.Pool(processes = NUM_PROC)
            result = numpy.atleast_2d( pool.map(pw,xrange(0,NUM_PROC)) ).astype(numpy.float)
            pool.close()
            pool.join()
        else:
            result = numpy.atleast_2d([r for r in itertools.imap(pw,xrange(0,NUM_PROC))]).astype(numpy.float)
            
        finish = time.clock()
        
        print 'Finished {0} games in {1}'.format(nGamesTot,finish-start)
        
        keys.append(A)
        
        result = numpy.reshape( result,(result.shape[0]*result.shape[1],result.shape[2]) )
        
        results.append(result)

    outFileZ = outDir + "results_A_{0}_{1}_{2}_nGames_{3}".format(aStart,aStop,aStep,nGamesTot)
    numpy.savez(outFileZ,results = numpy.dstack(results), A = keys, nGames = nGamesTot)    
    
    print 'Finished.'

if __name__ == "__main__":
    main()    