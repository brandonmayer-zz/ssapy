from ssapy.pricePrediction.util import ksStat, klDiv
from ssapy.pricePrediction.hist import hist
from ssapy.agents.agentFactory import agentFactory

import numpy
import matplotlib.pyplot as plt

import multiprocessing
import time
import os
import glob
import json
import sys
import copy
import shutil

def bidHelper(**kwargs):
    agent = kwargs.get('agent')
    dist  = kwargs.get('bayesMargDist')
    
    return agent.bid(margDistPrediction = dist)

def bayesSCPP(**kwargs):
    oDir      = kwargs.get('oDir')
    agentType = kwargs.get('agentType')
    nAgents   = kwargs.get('nAgents',8)
    m         = kwargs.get('m',5)
    minPrice  = kwargs.get('minPrice',0)
    maxPrice  = kwargs.get('maxPrice',50)
    maxSim    = kwargs.get('maxSim', 1000)
    nGames    = kwargs.get('nGames', 100)
    parallel  = kwargs.get('parallel', False)
    nProc     = kwargs.get('nProc', multiprocessing.cpu_count() - 1)
    tol       = kwargs.get('tol',0.001)
    plot      = kwargs.get('plot', True)
    log       = kwargs.get('log', True)
    verbose   = kwargs.get('verbose', True)
    
    if not oDir:
        str = "-----ERROR-----\n" +\
              "In bayesSCPP(...)\n" +\
              "Must Provide output directory\n"
        raise ValueError(str)
    
    if plot:
        pltDir = os.path.join(oDir,'plots')
        if not os.path.exists(pltDir):
            os.makedirs(pltDir)
        else:
            shutil.rmtree(pltDir,ignore_errors=True)
            os.makedirs(pltDir)
    
    if not os.path.exists(oDir):
        os.makedirs(oDir)
        
    if log:
        logFile = os.path.join(oDir,'bayesSCPP_{0}.txt'.format(agentType))
        if os.path.exists(logFile):
            os.remove(logFile)
            
        with open(logFile,'a') as f:
            f.write("oDir      = {0}\n".format(oDir))
            f.write("agentType = {0}\n".format(agentType))
            f.write("nAgents   = {0}\n".format(nAgents))
            f.write("tol       = {0}\n".format(tol))
            f.write("m         = {0}\n".format(m))
            f.write("minPrice  = {0}\n".format(minPrice))
            f.write("maxPrice  = {0}\n".format(maxPrice))
            f.write("maxSim    = {0}\n".format(maxSim))
            f.write("nGames    = {0}\n".format(nGames))
            f.write("parallel  = {0}\n".format(parallel))
            f.write("plot      = {0}\n".format(plot))
        
    if verbose:
        print "oDir      = {0}".format(oDir)
        print "agentType = {0}".format(agentType)
        print "nAgents   = {0}".format(nAgents)
        print "tol       = {0}".format(tol)
        print "m         = {0}".format(m)
        print "minPrice  = {0}".format(minPrice)
        print "maxPrice  = {0}".format(maxPrice)
        print "maxSim    = {0}".format(maxSim)
        print "nGames    = {0}".format(nGames)
        print "parallel  = {0}".format(parallel)
        print "plot      = {0}".format(plot)
    
    
    currHist = hist()
    if plot:
        oFile = os.path.join(pltDir,'bayesSCPP_{0}_{1}.png'.format(agentType,0))
        title='bayesSCPP, {0}, Initial Distribution'.format(agentType)
        currHist.bayesMargDistSCPP().graphPdfToFile(fname = oFile,
                                                    title=title)
    
    klList = []
    ksList = []
    
    agentFactoryParams = {'agentType' : agentType,
                          'm'         : m,
                          'minPrice'  : minPrice,
                          'maxPrice'  : maxPrice}

    for sim in xrange(maxSim):
        oldHist = copy.deepcopy(currHist)
        
        for i in xrange(nGames):
            agentList = [agentFactory(**agentFactoryParams) for i in xrange(nAgents)]
            
            if parallel:
                pool = multiprocessing.Pool(nProc)
                
                bayesMarg = currHist.bayesMargDistSCPP()
                
                results = [pool.apply_async(bidHelper, kwds = {'agent': agent, 'bayesMargDist': bayesMarg} ) for agent in agentList]
                
                pool.close()
                
                pool.join()
                
                bids = numpy.zeros((nAgents,m))
                
                for idx,r in enumerate(results):
                    bids[idx,:] = r.get()
                    r._value = []
                    
            else:
                bids = numpy.atleast_2d([agent.bid(margDistPrediction = currHist.bayesMargDistSCPP()) for agent in agentList])
                
            winningBids = numpy.max(bids,0)
            for idx, wb in enumerate(winningBids):
                currHist.upcount(idx,wb,mag=1)
#            [currHist.upcount(idx, wb, mag=1) for idx, wb in enumerate(winningBids)]
        
        klList.append(klDiv(currHist.bayesMargDistSCPP(), oldHist.bayesMargDistSCPP()))
        
        ksList.append(ksStat(currHist.bayesMargDistSCPP(), oldHist.bayesMargDistSCPP()))
        
        if verbose:
            print ''
            print 'itr = {0}'.format(sim+1)
            print '\tNumber of Games = {0}'.format((sim+1)*nGames)
            print '\tkld             = {0}'.format(klList[-1])
            print '\tks              = {0}'.format(ksList[-1])
            
        
        if plot:
            oPlot = os.path.join(pltDir,'bayesSCPP_{0}_{1}.png'.format(agentType,(sim+1)*nGames))
            title='BayesSCPP straightMU8, klD = {0:.6}, ks = {1:.6} itr = {2}'.format(klList[-1],ksList[-1],(sim+1)*nGames)
            currHist.bayesMargDistSCPP().graphPdfToFile(fname = oPlot, title=title)
        
        if klList[-1] < tol:
            break
      
    if log:  
        with open(logFile,'a') as f:
            f.write('Done after {0} games ({1} iterations)\n'.format((sim+1)*nGames,sim))
            f.write('kl = {0}\n'.format(klList))
            f.write('ks = {0}\n'.format(ksList))
        
    klFile = os.path.join(oDir,'kl.json')
    with open(klFile,'w') as f:
        json.dump(klList,f)
        
    ksFile = os.path.join(oDir,'ks.json')
    with open(ksFile,'w') as f:
        json.dump(ksList,f)
        
    if verbose:
        print 'Done'
        

def agentTypeListBayesSCPP(**kwargs):
    agentTypeList = kwargs.get('agentTypeList')
    oDir          = kwargs.get('oDir')
    nAgents       = kwargs.get('nAgents',8)
    m             = kwargs.get('m',5)
    minPrice      = kwargs.get('minPrice',0)
    maxPrice      = kwargs.get('maxPrice',50)
    maxSim        = kwargs.get('maxSim', 1000)
    nGames        = kwargs.get('nGames', 100)
    parallel      = kwargs.get('parallel', True)
    nProc         = kwargs.get('nProc', multiprocessing.cpu_count() - 1)
    tol           = kwargs.get('tol',0.001)
    plot          = kwargs.get('plot', True)
    log           = kwargs.get('log', True)
    verbose       = kwargs.get('verbose', True)
    
    if not oDir:
        str = "-----ERROR-----\n" +\
              "In bayesSCPP(...)\n" +\
              "Must Provide output directory\n"
        raise ValueError(str)
    oDir = os.path.realpath(oDir)
    
    pool = multiprocessing.Pool(nProc)
    
    for agentType in agentTypeList:
        od = os.path.join(oDir,agentType)
        kwa = {'oDir': od,
               'nAgents': nAgents,
               'm':m,
               'minPrice':minPrice,
               'maxPrice':maxPrice,
               'maxSim':maxSim,
               'nGames':nGames,
               'parallel':False,
               'tol':tol,
               'plot':plot,
               'log':log,
               'verbose':verbose}
        
        pool.apply_async(bayesSCPP, kwds = kwa)
        
    pool.close()
        
    pool.join()
    
    print 'Done'
        
    
        
        
        
    