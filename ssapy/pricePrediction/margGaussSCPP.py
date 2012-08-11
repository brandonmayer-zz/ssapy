import numpy
from sklearn import mixture
from ssapy.multiprocessingAdaptor import Consumer
from ssapy.agents.agentFactory import margAgentFactory
from ssapy.pricePrediction.margDistSCPP import margDistSCPP
from ssapy.pricePrediction.util import aicFit, drawGMM

import matplotlib.pyplot as plt
from scipy.stats import norm

import json
import multiprocessing
import os 
import time
import random
import itertools
def plotClfList(**kwargs):
    
    clfList = kwargs.get('clfList')
    colors  = kwargs.get('colors',['r-o,','b-*','g-^','m-<','c-.'])
    
    colorCycle = itertools.cycle(colors)
    
    plt.figure()
    plt.plt() 

def simulateAuctionGMM( **kwargs ):
    agentType  = kwargs.get('agentType')
    nAgents    = kwargs.get('nAgents',8)
    clfList    = kwargs.get('clfList')
    nSamples   = kwargs.get('nSampeles',8)
    nGames     = kwargs.get('nGames')
    minPrice   = kwargs.get('minPrice',0)
    maxPrice   = kwargs.get('maxPrice',50)
    m          = kwargs.get('m',5)
    
        
    winningBids = numpy.zeros((nGames,m))
    
    for g in xrange(nGames):
        
        agentList = [margAgentFactory(agentType = agentType, m = m) for i in xrange(nAgents)]
        
        if clfList == None:
            samples = ((maxPrice - minPrice) *numpy.random.rand(nAgents,nSamples,m)) + minPrice
            expectedPrices = numpy.mean(samples,1)
            bids = numpy.atleast_2d([agent.bid(pointPricePrediction = expectedPrices[i,:]) for idx, agent in enumerate(agentList)])
                    
        elif isinstance(clfList, list):
            
            bids = numpy.zeros((nAgents,m))
            
            for agentIdx, agent in enumerate(agentList):
                expectedPrices = numpy.zeros(m)
                for clfIdx, clf in enumerate(clfList):
                    samples = drawGMM(clf, nSamples)
                    expectedPrices[clfIdx] = numpy.mean(samples)
                bids[agentIdx,:] = agent.bid(pointPricePrediction = expectedPrices)
            
        else:
            raise ValueError("Unknown price dist type.") 
        
        winningBids[g,:] = numpy.max(bids,0)
        
    return winningBids

def margGaussSCPP(**kwargs):
    oDir = kwargs.get('oDir')
    if not oDir:
        raise ValueError("Must provide output Directory")
    oDir = os.path.realpath(oDir)

def main():
    agentType = "straightMV"
    nAgents   = 8
    nGames = 10
    m = 5
    
    clfList = None
    
    for g in xrange(nGames):
        
        winningBids = simulateAuctionGMM(agentType = agentType,
                                         nAgents   = nAgents,
                                         clfList   = clfList,
                                         nSamples  = 8,
                                         nGames    = nGames,
                                         m         = m)
        
        clfList = []
        for i in xrange(winningBids.shape[1]):
            clf, aicList, compRange = aicFit(winningBids[:,i])
            clfList.append(clf)
    
    pass
    
if __name__ == "__main__":
    main()
    