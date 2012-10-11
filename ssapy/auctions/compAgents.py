from ssapy.agents.agentFactory import agentFactory
from ssapy.auctions import simulateAuction
from ssapy.auctions.simultaneousAuction import simultaneousAuction

import matplotlib.pyplot as plt
import numpy

import multiprocessing
import pickle
import os

def comp2Agents(**kwargs):
    oDir         = kwargs.get('oDir')
    pp1          = kwargs.get('pp1')
    n1           = kwargs.get('n1',4)
    pp2          = kwargs.get('pp2')
    n2           = kwargs.get('n2',4)
    agentType1   = kwargs.get('agentType1')
    agentType2   = kwargs.get('agentType2')
    m            = kwargs.get('m',5)
    minValuation = kwargs.get('minValuation',0)
    maxValuation = kwargs.get('maxValuation',50)
    nGames       = kwargs.get('nGames',1000)
    parallel     = kwargs.get('parallel',True)
    nProc        = kwargs.get('nProc', multiprocessing.cpu_count() - 1)
    verbose      = kwargs.get('verbose', True)
    
    
    auction = simultaneousAuction( m       = m,
                                   nPrice  = 2,
                                   reserve = 0)
    
    for i in xrange(n1):
        agent = agentFactory(agentType = agentType1, 
                             m         = m, 
                             vmin      = minValuation, 
                             vmax      = maxValuation  )
        
        agent.pricePrediction = pp1
        
        
        auction.attachAgents(agent)
                             
    for i in xrange(n2):
        agent = agentFactory(agentType = agentType2, 
                             m         = m, 
                             vmin      = minValuation, 
                             vmax      = maxValuation  )
        
        agent.pricePrediction = pp2
        
        auction.attachAgents(agent)
    
    agentSurplus = numpy.zeros((nGames,n1+n2))
    
    for itr in xrange(nGames):
        if verbose:
            print 'Simulating {0} out of {1} auctions'.format(itr,nGames)
        [agent.randomValuation() for agent in auction.agentList]
        
        auction.runAuction()
        
        auction.notifyAgents()
        
        surplus = auction.agentSurplus()
        
        agentSurplus[itr,:] = surplus
        
    if oDir:
        oDir = os.path.realpath(oDir)
        if not os.path.exists(oDir):
            os.makedirs(oDir)
            
        sFile = os.path.join(oDir,'{0}_{1}_agentSurplus.txt'.format(agentType1,agentType2))
        
        numpy.savetxt(sFile, agentSurplus) 
        
    return agentSurplus
    
    
