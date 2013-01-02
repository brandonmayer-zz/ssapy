from auctionSimulator.hw4.auctions.simultaneousAuction import *
from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.agents.straightMU import *
from auctionSimulator.hw4.agents.targetPriceDist import *

import numpy
import matplotlib.pyplot as plt
import multiprocessing
import time
import itertools

class parallelWorker(object):
    def __init__(self, margDistPrediction = None, nGames = 100):
        numpy.testing.assert_(isinstance(margDistPrediction, margDistSCPP),
                              msg='Must Specify a marginal price prediction distribution')
        
        self.margDistPrediction = margDistPrediction
        self.nGames = nGames
        
    def __call__(self, dummy = 0):
        
        agentSurplus = []
        for i in xrange(self.nGames):
#            print 'Iteration = {0}'.format(i)
            
            agentList = []
            
            riskAware1 = riskAware(margDistPricePrediction = self.margDistPrediction,
                                   A                       = 0,
                                   name                    = 'riskAware_A={0}'.format(0))
        
            
            agentList.append(targetPriceDist(margDistPricePrediction = self.margDistPrediction,
                                             v                       = riskAware1.v,
                                             name                    = 'targetPrice',
                                            l                        = riskAware1.l))
            
            agentList.append(riskAware1)
        
            for A in xrange(2,30,2):
                agentList.append(riskAware(margDistPricePrediction = self.margDistPrediction,
                                           A                       = A,
                                           name                    = 'riskAware_A={0}'.format(A),
                                           v                       = riskAware1.v,
                                           l                       = riskAware1.l))
                
            auction = simultaneousAuction(agentList)
            
            auction.runAuction()
            
            auction.notifyAgents()
            
            agentSurplus.append(auction.agentSurplus())
            
        return numpy.atleast_2d(agentSurplus).astype(numpy.float)
        

def main():
    nGames = 100
    
    NUM_PROC = 10
    
    margDistPkl = "C:\\bmProjects\\courses\\fall2011\\csci2951\\" +\
                  "auctionSimulator\\hw4\\pricePrediction\\margDistPredictions\\" +\
                  "distPricePrediction_straightMU_10000_2011_12_4_1323040769.pkl"
    
    margDistPrediction=margDistSCPP()
    
    margDistPrediction.loadPickle(margDistPkl)
    
    pw = parallelWorker(margDistPrediction = margDistPrediction, 
                        nGames             = nGames)
    
    pool = multiprocessing.Pool(processes = NUM_PROC)
    
    parallel = True
    
    print 'Computing Result'
    
    start = time.clock()    
    if parallel:
        result = numpy.atleast_2d( pool.map(pw,xrange(0,NUM_PROC)) ).astype(numpy.float)
        
        pool.close()
        pool.join()
    else:
        result = numpy.atleast_2d([r for r in itertools.imap(pw,xrange(0,NUM_PROC))]).astype(numpy.float)
    finish = time.clock()
    
    print 'Finished {0} games in {1}'.format(nGames*NUM_PROC,finish-start)
     
    result = numpy.reshape( result,(result.shape[0]*result.shape[1],result.shape[2]) )
        
    surplusMean = numpy.mean(result,0)
    
    # graph the results
    agentNames = []
    agentNames.append('targetPrice')
    for A in xrange(0,30,2):
        agentNames.append('riskAware_A={0}'.format(A)) 
         
    ind = numpy.arange(len(agentNames))+.5
        
    width = 0.35
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(ind,surplusMean,width)
    plt.xticks(ind+width,tuple(agentNames))
    plt.ylabel('Average Surplus')
    plt.title('Symmetric Valuation, $\lambda$, and Distribution Prediction {0} games'.format(nGames*NUM_PROC))
    
    plt.show()
    
if __name__ == "__main__":
    main()