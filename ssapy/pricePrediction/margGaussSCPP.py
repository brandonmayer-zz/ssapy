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
import argparse

def plotClfList(**kwargs):
    
    clfList = kwargs.get('clfList')
    colors  = kwargs.get('colors',['r-o,','b-*','g-^','m-<','c-.'])
    
    colorCycle = itertools.cycle(colors)
    
    plt.figure()
    plt.plt() 
    
def apprxKL(clf1, clf2, nSamples = 1000):
    
    kl = 0
    for idx, c1 in enumerate(clf1):
        c2 = clf2[idx]
        samples1 = clf1.sample(nSamples)
        samples2 = clf2.sample(nSamples)
        f1 = c1.eval(samples1)
        g1 = c2.eval(samples1)
        f2 = c1.eval(samples2)
        g2 = c2.eval(samples2)
        d1 = (1/nSamples)*sum(f1/g1)
        d2 = (1/nSamples)*sum(g2/f2)
        kl += (d1 + d2)

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
    
    agentType = kwargs.get('agentType',"straightMV")
    nAgents   = kwargs.get('nAgnets',8)
    nGames    = kwargs.get('nGames',10)
    m         = kwargs.get('m',5)
    minPrice  = kwargs.get('minPrice',0)
    maxPrice  = kwargs.get('maxPrice',50)
    serial    = kwargs.get('serial',False)
    klSamples = kwargs.get('klSamples',1000)
    verbose   = kwargs.get('verbose',True) 
    
    if verbose:
        print 'agentType = {0}'.format(agentType)
        print 'nAgents   = {0}'.format(nAgents)
        print 'nGames    = {0}'.format(nGames)
        print 'm         = {0}'.format(m)
        print 'minPrice  = {0}'.format(minPrice)
        print 'maxPrice  = {0}'.format(maxPrice)
        print 'klSamples = {0}'.format(klSamples)
        
    
    binEdges  = numpy.arange(minPrice,maxPrice+1,1)
    tempDist = []
    p = float(1)/round(maxPrice - minPrice)
    a = [p]*(maxPrice - minPrice)
    for i in xrange(m):
        tempDist.append((numpy.atleast_1d(a), numpy.atleast_1d(binEdges)))
        
    currentDist = margDistSCPP(tempDist)
    
    clfList = None
    clfPrev = None
    if serial:
        
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
                
            if clfPrev:
                kl = apprxKl(clfList, clfPrev, nSamples)
        
            clfPrev = clfList
        else:
            pass
    
    

def main():
       
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', "--oDir",        action = "store", type = str,   dest = "oDir")
    parser.add_argument('-at', "--agentType",  action = "store", type = str,   dest = "agentType", default = "straightMV")
    parser.add_argument('-na',"--nAgents",     action = "store", type = int,   dest = "nAgents",   default = 8)
    parser.add_argument('-ng',"--nGames",      action = "store", type = int,   dest = "nGames",    default = 10000 )
    parser.add_argument('-v', "--verbose",     action = "store", type = bool,  dest = "verbose",   default = True)
    parser.add_argument('-s', "--serial",      action = "store", type = bool,  dest = "serial",    default = False)
    parser.add_argument('-np',"--nProc",       action = "store", type = int,   dest = "nProc",     default = multiprocessing.cpu_count() - 1)
    parser.add_argument('-kls', "--klSamples", action = "store", type = int,  dest = "klSamples", defulat = 1000)
    parser.add_argument('-mip', "--minPrice",  action = "store", type = int,   dest = "minPrice",  default = 0)
    parser.add_argument('-map', "--maxPrice",  action = "store", type = int,   dest = "maxPrice",  default = 50)
    parser.add_argument("--serial",            action = "store", type = str,   dest = "serial",    default = False)
    
    opts = parser.parse_args()
    
    oDir      = opts.oDir
    agentType = opts.agentType
    nAgents   = opts.nAgents
    nGames    = opts.nGames
    verbose   = opts.verbose
    minPrice  = opts.minPrice
    maxPrice  = opts.maxPrice
    
    margGaussSCPP(oDir      = oDir,
                  agentType = agentType,
                  nAgents   = nAgents,
                  nGames    = nGames,
                  minPrice  = minPrice,
                  maxPrice  = maxPrice,
                  serial    = serial,
                  verbose   = verbose)
    
    
    
    
if __name__ == "__main__":
    main()
