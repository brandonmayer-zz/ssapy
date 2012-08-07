import numpy
from sklearn import mixture
from ssapy.multiprocessingAdaptor import Consumer
from ssapy.agents.agentFactory import margAgentFactory
from ssapy.pricePrediction.margDistSCPP import margDistSCPP

import matplotlib.pyplot as plt
from scipy.stats import norm

import json
import multiprocessing
import os 
import time

def simulateAuctionGMM( **kwargs ):
    agentType  = kwargs.get('agentType')
    nAgnets    = kwargs.get('nAgents',8)
    priceDist  = kwargs.get('priceDist')
    nSamples   = kwargs.get('nSampeles',8)
    nGames     = kwargs.get('nGames')
    minPrice   = kwargs.get('minPrice')
    maxPrice   = kwargs.get('maxPrice')
#    m          = margDist.m
    
    
    m = None
    if isinstance(priceDist,margDistSCPP):
        m = priceDist.m
    elif isinstance(priceDist,list):
        m = len(priceDist)
    else:
        raise ValueError("simulateAuctionGMM --- Unknown priceDist type")
    
    winningBids = numpy.zeros((nGames,m))
    
    for g in xrange(nGames):
        agentList = [margAgentFactory(agentType = agentType, m = m) for i in xrange(nAgents)]
        
        if isinstance(priceDist,'margDistSCPP'):
            bids = numpy.atleast_2d([agent.bid(margDistPrediction = margDist) for agent in agentList])
            
        elif isintance(priceDict, list):
            
            for agent in agentList:
                expectedPrice = numpy.zeros((m,1))
                for idx, gmm in enumerate(priceDist):
                    if not isinstance(gmm,mixture.GMM):
                        raise ValueError("simulateAuctonGMM --- must provide a list of GMMs")
                    samples = []
                    for i in xrange(nSamples):
                        s  = gmm.sample(1)
                        while s > maxPrice or s < minPrice:
                            s = gmm.sample(1)
                        samples.append(s)
                        
                    expectedPrice[idx] = numpy.mean(samples)
            
            bins = numpy.atleast_2d(agent.bid(expectedPrices = expectedPrice) for agent in agentList) 
        
        winningBids[g,:] = numpy.max(bids,0)
        
    return winningBids

def main():
    agentType = "straightMU"
    nAgents   = 8
    nGames = 10
    m = 5
    
    
    mu = numpy.random.rand(m)*10 + 50
    sig = numpy.random.rand(m)*5 + 10
    ns = 300
    X = numpy.zeros((ns,m))
    
    for i in xrange(m):
        X[:,i] = numpy.random.normal(loc=mu[i],scale = sig[i],size=ns)
        
    pricePrediction = []
    [pricePrediction.append(mixture.GMM(n_components=5)) for i in xrange(m)]
    
    for idx, clf in enumerate(pricePrediction):
        clf.fit(X[:,idx])
        
    
    xax = numpy.linspace(-100, 100, 10000)
    
    
    for idx,clf in enumerate(pricePrediction):
        plt.subplot(int(float("{0}1{1}".format(m,idx))))
        a = clf.eval(xax)[0]
        samp = clf.sample(100)
        Z = numpy.exp(a)
        plt.plot(xax,Z,label='GMM')
        plt.plot(samp,[0]*len(samp),'r*',label='test')
        leg = ax.legend(fancybox=True)
        leg.get_frame().set_alpha(0.5)
        
    plt.show()
    
    simulateAuctionGMM(agentType = agentType,
                       nAgents   = nAgents,
                       priceDist = pricePrediction,
                       nSamples  = 8,
                       nGames    = nGames)
                       
    
    
    pass
    
if __name__ == "__main__":
    main()
    