import numpy
from sklearn import mixture
from ssapy.multiprocessingAdaptor import Consumer
from ssapy.agents.agentFactory import margAgentFactory
from ssapy.pricePrediction.margDistSCPP import margDistSCPP
from ssapy.pricePrediction.util import aicFit, drawGMM, plotMargGMM, apprxMargKL
from ssapy.pricePrediction.util import simulateAuctionJointGMM

import matplotlib.pyplot as plt
from scipy.stats import norm

import json
import multiprocessing
import os 
import time
import random
import itertools
import argparse
import pickle

def jointGaussSCPP(**kwargs):
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
    nProc     = kwargs.get('nProc',multiprocessing.cpu_count()-1)
    minCovar  = kwargs.get('minCovar',9)
    covarType = kwargs.get('covarType','full')
    savePkl   = kwargs.get('savePkl',True)
    verbose   = kwargs.get('verbose',True) 
    
    if verbose:
        print 'agentType = {0}'.format(agentType)
        print 'nAgents   = {0}'.format(nAgents)
        print 'nGames    = {0}'.format(nGames)
        print 'm         = {0}'.format(m)
        print 'minPrice  = {0}'.format(minPrice)
        print 'maxPrice  = {0}'.format(maxPrice)
        print 'maxItr    = {0}'.format(maxItr)
        print 'tol       = {0}'.format(tol)
        print 'klSamples = {0}'.format(klSamples)
        print 'pltDist   = {0}'.format(pltDist)
        print 'serial    = {0}'.format(serial)
        print 'nProc     = {0}'.format(nProc)
        print 'minCovar  = {0}'.format(minCovar)
        
        
    
    if savePkl:
        pklDir = os.path.join(oDir, 'gmmPkl')
        if not os.path.exists(pklDir):
            os.makedirs(pklDir)
        
    clfCurr = None
    clfPrev = None
    klList = []
    for itr in xrange(maxItr):
        if verbose:
            print 
            print 'Iteration = {0}'.format(itr)
            
        if serial:
            winningBids = simulateAuctionJointGMM(agentType = agentType,
                                             nAgents   = nAgents,
                                             clf       = clfCurr,
                                             nSamples  = nSamples,
                                             nGames    = nGames,
                                             m         = m)
        else:
            pool = multiprocessing.Pool(nProc)
            
            winningBids = numpy.zeros((nGames,m))
            nGameList = [nGames//nProc]*nProc
            nGameList[-1] += (nGames % nProc)
            
            results = []
            for p in xrange(nProc):
                ka = {'agentType':agentType, 
                      'nAgents':nAgents,
                      'clf':clfCurr,
                      'nSamples':nSamples,
                      'nGames':nGameList[p],'m':m}
                results.append(pool.apply_async(simulateAuctionJointGMM, kwds = ka))
            
            pool.close()
            
            pool.join()
            
            start_row = 0
            end_row = 0
            for idx, r in enumerate(results):
                end_row += nGameList[idx]
                winningBids[start_row:end_row,:] = r.get()
                results[idx]._value = []
                start_row = end_row
        
        
        clfCurr, aicList, compRange = aicFit(winningBids, minCovar = minCovar)    
        
        if savePkl:
            pklFile = os.path.join(pklDir,'gmm_{0}.pkl'.format(itr))
            with open(pklFile,'wb') as f:
                pickle.dump(clfCurr, f)
        
        if clfPrev:
            kl = apprxMargKL(clfCurr, clfPrev, klSamples)
            klList.append(kl)
            
#        if pltDist:
#            pltDir = os.path.join(oDir,'scppPlts')
#            if not os.path.exists(pltDir):
#                os.makedirs(pltDir)
#            oFile = os.path.join(oDir, 'scppPlts', 'gaussMargSCPP_{0}.png'.format(itr))
#            if klList: 
#                title = "margGaussSCPP itr = {0} kld = {1}".format(itr,klList[-1])
#            else:
#                title = "margGaussSCPP itr = {0}".format(itr)
#            plotMargGMM(clfList = clfList, 
#                        oFile = oFile, 
#                        minPrice = minPrice, 
#                        maxPrice = maxPrice,
#                        title = title)
            
        if klList:
            if klList[-1] < tol:
                klFile = os.path.join(oDir,'kld.json')
                with open(klFile,'w') as f:
                    json.dump(klList,f)
                    
                print 'kld = {0} < tol = {1}'.format(klList[-1],tol)
                print 'DONE'
                break
    
        clfPrev = clfCurr
    
     