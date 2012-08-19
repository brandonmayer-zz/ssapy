from ssapy.agents.straightMU import *
from ssapy.pricePrediction.hist import *
from ssapy.auctions.simultaneousAuction import *
from ssapy.pricePrediction.util import ksStatistic

import numpy
import matplotlib.pyplot as plt
import time
import os
import copy
import glob
import json
    
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
    nGames = 100
    parallel = False
    tol = .001
    outDir = os.path.realpath('C:/auctionResearch/experiments/bayesSCPP_straightMU8_{0}_{1}_{2}'.format(nAgents,m,tol))
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    
    currHist = hist()
    
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    
    sim = 0
    cs = ['y--p', 'm-*', 'r-o','y-^','y-*']
    outfile = os.path.join(outDir,'bayesSCPP_itr_{0}.png'.format(sim))
    title='Bayes SCPP, straightMU8, klD = {0} Number of Samples = {1}'.format(0,sim*nGames)
    currHist.bayesMargDistSCPP().graphPdfToFile(fname=outfile,
                                                colorStyles=cs,
                                                title=title)
    
    klList = []
    ksList = []
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
        klList.append(kl)
        ks = ksStatistic(currHist.bayesMargDistSCPP(), oldHist.bayesMargDistSCPP())
        ksList.append(ks)
        
        outfile = os.path.join(outDir,'bayesSCPP_itr_{0}.png'.format(sim))
        title='BayesSCPP straightMU8, klD = {0:.6}, ks = {1:.6} itr = {2}'.format(kl,ks,sim*nGames)
        currHist.bayesMargDistSCPP().graphPdfToFile(fname=outfile,
                                                    colorStyles=cs,
                                                    title=title)
        print 'saving plot to: {0}'.format(outfile)
        print'\tkl = {0}'.format(kl)
        print ''
        if kl < tol:
            print 'Done!'
            print 'number of iterations = {0}'.format(sim)
            done = True
            
    plt.subplot(211)
    plt.plot(range(0,len(klList)*100,100),klList,'r-')
    plt.title('KL Divergence')
    
    plt.subplot(212)
    plt.plot(range(0,len(klList)*100,100),ksList,'b-')
    plt.title('KS Statistic')
    
    fname = os.path.join(outDir,'error.png')
    plt.savefig(fname)
    
    ksListName = os.path.join(outDir,'ksList.json')
    with open(ksListName,'w') as f:
        json.dump(ksList,f)
        
    klListName = os.path.join(outDir,'klList.json')
    with open(klListName,'w') as f:
        json.dump(klList,f)
        
#        plt.show()
#    currHist.bayesMargDistSCPP().graphPdf()
                

        
    
    
        
        
if __name__ == "__main__":
    main()    