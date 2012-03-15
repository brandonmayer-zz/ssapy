from aucSim.agents.straightMU import *
from aucSim.pricePrediction.hist import *
from aucSim.auctions.simultaneousAuction import *

import numpy
import time
import os
import copy
    
def klDiv(margDist1, margDist2):
    assert isinstance(margDist1, margDistSCPP) and\
            isinstance(margDist2, margDistSCPP),\
        "margDist1 and margDist2 must be instances of margDistSCPP"
        
    numpy.testing.assert_equal(margDist1.m, 
                               margDist2.m)
    
    kldSum = 0.0
    for idx in xrange(margDist1.m):
        # test that the distributions are over the same bin indices
        # if they are not this calculation is meaninless
        numpy.testing.assert_equal(margDist1.data[idx][1],
                                   margDist2.data[idx][1])
        
        #test that the distributions have the same number of bins
        numpy.testing.assert_equal(len(margDist1.data[idx][0]),
                                   len(margDist2.data[idx][0]))
        
        
        kldSum += numpy.sum(margDist1.data[idx][0] * (numpy.log(margDist1.data[idx][0]) 
                                               - numpy.log(margDist2.data[idx][0]))) 
        
    return kldSum
                               
    
    
def main():
    nAgents  = 8
    m        = 5
    minPrice = 0
    maxPrice = 50
    delta = 1
    maxSim = 1000
    nGames = 1000
    parallel = False
    outDir = 'E:/research/auction/bayesSCPP/exp1/'
    tol = .1
    
    currHist = hist()
    
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    
    sim = 0
    done = False
    while sim < maxSim and not done:
        sim+=1
        oldHist = copy.deepcopy(currHist)
        print'sim = {0}'.format(sim)
        
        for i in xrange(nGames):
            print'\t itr = {0}'.format(i)
            agentList = [straightMU8(m=m) for j in xrange(nAgents)]
            
            bids = numpy.atleast_2d([agent.bid(margDistPrediction = currHist.bayesMargDistSCPP()) 
                                     for agent in agentList])
                
            winningBids = numpy.max(bids,0)
            
            for i in xrange(len(winningBids)):
                currHist.upcount(i, winningBids[i], mag=1)
                
#        oldHist.bayesMargDistSCPP().graphPdf()
                
        #calculate the KL divergence between the old and new distributions
        kl = klDiv(currHist.bayesMargDistSCPP(),oldHist.bayesMargDistSCPP())
        print'\tkl = {0}'.format(kl)
        print ''
        if kl < tol:
            print 'Done!'
            print 'number of iterations = {0}'.format(sim)
            done = True
            
    currHist.bayesMargDistSCPP().graphPdf()
                

        
    
    
        
        
if __name__ == "__main__":
    main()    