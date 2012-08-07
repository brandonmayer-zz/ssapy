import numpy
from sklearn import mixture
from ssapy.multiprocessingAdaptor import Consumer
from ssapy.agents.agentFactory import margAgentFactory
from ssapy.pricePrediction.margDistSCPP import margDistSCPP

import json
import multiprocessing
import os 
import time

def simulateAuctionGMM( **kwargs ):
    agentType  = kwargs.get('agentType')
    nAgnets    = kwargs.get('nAgents')
    priceDist  = kwargs.get('priceDist')
    nSamples   = kwargs.get('nSampeles',8)
    nGames     = kwargs.get('nGames')
    m          = margDist.m
    
    winningBids = numpy.zeros((nGames,m))
    
    
    
    for g in xrange(nGames):
        agentList = [margAgentFactory(agentType = agentType, m = m) for i in xrange(nAgents)]
        
        if isinstance(priceDist,'margDistSCPP'):
            bids = numpy.atleast_2d([agent.bid(margDistPrediction = margDist) for agent in agentList])
            
        elif isintance(priceDict, mixture.GMM):
            pass
        
        winningBids[g,:] = numpy.max(bids,0)
        
    return winningBids
    