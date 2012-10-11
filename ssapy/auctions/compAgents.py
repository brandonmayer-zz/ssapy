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
    
    if verbose:
        print ''
        print 'In comp2Agents(...)'
        print 'oDir         = {0}'.format(oDir)
        
        print 'agentType1   = {0}'.format(agentType1)
        print 'n1           = {0}'.format(n1)
        
        print 'agentType2   = {0}'.format(agentType2)
        print 'n2           = {0}'.format(n2)
        
        print 'm            = {0}'.format(m)
        print 'nGames       = {0}'.format(nGames)
        print 'minValuation = {0}'.format(minValuation)
        print 'maxValuation = {0}'.format(maxValuation)
        
        print ''  
    
    
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
        
        if verbose:
            for idx, agent in enumerate(auction.agentList):
                print 'agent[{0}] = {1} ; l = {2}, v = {3}'.format(idx, agent.type(), agent.l, agent.v)
        
        auction.runAuction()
        
        auction.notifyAgents()
        
        surplus = auction.agentSurplus()
        
        agentSurplus[itr,:] = surplus
        
        if verbose:
            print 'Agent Surplus = {0}'.format(surplus)
        
    if oDir:
        oDir = os.path.realpath(oDir)
        if not os.path.exists(oDir):
            os.makedirs(oDir)
            
        sFile = os.path.join(oDir,'{0}_{1}_agentSurplus.txt'.format(agentType1,agentType2))
        
        numpy.savetxt(sFile, agentSurplus) 
        
    return agentSurplus
    
    
