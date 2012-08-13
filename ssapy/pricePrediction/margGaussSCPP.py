import numpy
from sklearn import mixture
from ssapy.multiprocessingAdaptor import Consumer
from ssapy.agents.agentFactory import margAgentFactory
from ssapy.pricePrediction.margDistSCPP import margDistSCPP
from ssapy.pricePrediction.util import aicFit, drawGMM, plotMargGMM, apprxMargKL

import matplotlib.pyplot as plt
from scipy.stats import norm

import json
import multiprocessing
import os 
import time
import random
import itertools
import argparse
    
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
    nSamples  = kwargs.get('nSamples',8)
    m         = kwargs.get('m',5)
    minPrice  = kwargs.get('minPrice',0)
    maxPrice  = kwargs.get('maxPrice',50)
    serial    = kwargs.get('serial',False)
    klSamples = kwargs.get('klSamples',1000)
    maxItr    = kwargs.get('maxItr', 100)
    tol       = kwargs.get('tol', 0.01)
    pltDist   = kwargs.get('pltDist',True)
    verbose   = kwargs.get('verbose',True) 
    nProc     = kwargs.get('nProc',multiprocessing.cpu_count()-1)
    
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
    
    for itr in xrange(maxItr):
        
        if serial:
            winningBids = simulateAuctionGMM(agentType = agentType,
                                             nAgents   = nAgents,
                                             clfList   = clfList,
                                             nSamples  = nSamples,
                                             nGames    = nGames,
                                             m         = m)
        else:
            pool = multiprocessing.Pool(nProc)
            
            winningBids = numpy.zeros((nGames,m))
            nGameList = [nGames//nProc]*nProc
            nGameList[-1] += (nGames % nProc)
            
            results = []
            for p in nProc:
                ka = {'agentType':agentType, 
                      'nAgents':nAgents,
                      'clfList':clfList,
                      'nSamples':nSamples,
                      'nGames':nGamesList[p],'m':m}
                results.append(pool.apply_async(simulateAuctionGMM, kwds = ka))
            
            pool.close()
            
            pool.join()
            
            start_row = 0
            end_row = 0
            for idx, r in enumerate(results):
                end_row += nGameList[idx]
                winningBids[start_row:(end_row-1),:] = r.get()
                results[idx]._value = []
                start_row = end_row
            
            pass
        
        
        clfList = []
        for i in xrange(winningBids.shape[1]):
            clf, aicList, compRange = aicFit(winningBids[:,i])
            clfList.append(clf)
            
        
            
        if pltDist:
            pltDir = os.path.join(oDir,'scppPlts')
            if not os.path.exists(pltDir):
                os.makedirs(pltDir)
            oFile = os.path.join(oDir, 'scppPlts', 'gaussMargSCPP_{0}.png'.format(itr))
            plotMargGMM(clfList = clfList, 
                        oFile = oFile, 
                        minPrice = minPrice, 
                        maxPrice = maxPrice,
                        title = "Marginal Gaussian SCPP itr = {0}".format(itr))
            
        if clfPrev:
            kl = apprxMargKL(clfList, clfPrev, klSamples)
            if kl < tol:
                print 'kld = {0} < tol = {1}'.format(kl,tol)
                break
    
        clfPrev = clfList
        
    
    

def main():
       
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', "--oDir",        action = "store", type = str,   dest = "oDir")
    parser.add_argument('-at', "--agentType",  action = "store", type = str,   dest = "agentType", default = "straightMV")
    parser.add_argument('-na',"--nAgents",     action = "store", type = int,   dest = "nAgents",   default = 8)
    parser.add_argument('-ng',"--nGames",      action = "store", type = int,   dest = "nGames",    default = 10000 )
    parser.add_argument('-v', "--verbose",     action = "store", type = bool,  dest = "verbose",   default = True)
    parser.add_argument('-s', "--serial",      action = "store", type = bool,  dest = "serial",    default = False)
    parser.add_argument('-np',"--nProc",       action = "store", type = int,   dest = "nProc",     default = multiprocessing.cpu_count() - 1)
    parser.add_argument('-kls', "--klSamples", action = "store", type = int,   dest = "klSamples", default = 1000)
    parser.add_argument('-mip', "--minPrice",  action = "store", type = int,   dest = "minPrice",  default = 0)
    parser.add_argument('-map', "--maxPrice",  action = "store", type = int,   dest = "maxPrice",  default = 50)
    parser.add_argument("--maxItr",            action = "store", type = int,   dest = "maxItr",    default = 100)
    parser.add_argument("--tol",               action = "store", type = int,   dest = "tol",       default = 0.01)
    parser.add_argument("--pltDist",           action = "store", type = bool,  dest = "pltDist",   default = True)
    
    
    opts = parser.parse_args()
    
    oDir      = opts.oDir
    agentType = opts.agentType
    nAgents   = opts.nAgents
    nGames    = opts.nGames
    verbose   = opts.verbose
    minPrice  = opts.minPrice
    maxPrice  = opts.maxPrice
    serial    = opts.serial
    maxItr    = opts.maxItr
    tol       = opts.tol
    pltDist   = opts.pltDist
    klSamples = opts.klSamples
    nProc     = opts.nProc
    
    margGaussSCPP(oDir      = oDir,
                  agentType = agentType,
                  nAgents   = nAgents,
                  nGames    = nGames,
                  minPrice  = minPrice,
                  maxPrice  = maxPrice,
                  serial    = serial,
                  maxItr    = maxItr,
                  tol       = tol,
                  pltDist   = pltDist,
                  klSamples = klSamples,
                  nProc     = nProc,
                  verbose   = verbose)
    
    
    
    
if __name__ == "__main__":
    main()
