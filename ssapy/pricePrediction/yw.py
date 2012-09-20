from ssapy.agents.straightMU import *
from ssapy.agents.targetMU import *
from ssapy.agents.targetMUS import *
from ssapy.agents.targetPriceDist import *
from ssapy.agents.riskAware import *

from ssapy.pricePrediction.util import klDiv, ksStat, updateDist, symmetricDPPworker

import matplotlib.pyplot as plot
import numpy
import multiprocessing
import time
import os
import json

def ywSCPP(**kwargs):
    oDir      = kwargs.get('oDir')
    if oDir == None:
        raise ValueError("Must provide oDir")
    oDir = os.path.realpath(oDir)
    
    agentType = kwargs.get('agentType', 'straightMU8')
    nAgents   = kwargs.get('nAgents',8)
    m         = kwargs.get('m',5)
    L         = kwargs.get('L',100)
    d         = kwargs.get('d', 0.01)
    g         = kwargs.get('g', 1000000)
    minPrice  = kwargs.get('minPrice',0)
    maxPrice  = kwargs.get('maxPrice',50)
    nSamples  = kwargs.get('nSamples',8)
    serial    = kwargs.get('serial', False)
    dampen    = kwargs.get('dampen', True)
    nProc     = kwargs.get('nProc', multiprocessing.cpu_count() - 1)
    verbose   = kwargs.get('verbose',True)
    pltItr    = kwargs.get('pltItr', True)
    
    
    if verbose:
        print'Computing Symmetric Self Confirming Point Price Prediction.'
        
        print'Agent Type                   = {0}'.format(agentType)
        
        print 'Termination Threshold (d)    = {0}'.format(d)
        
        print'Number of Iterations        = {0}'.format(L)
        
        print'Number of Games             = {0}'.format(g)
        
        print'Number of Items per Auction = {0}'.format(m)
        
        print 'Using Dampining             = {0}'.format(dampen)
        
        if serial:
            print 'Using serial implementation'
        else:
            print'Number of Parallel Cores    = {0}'.format(nProc)
            
        
        print'Output Directory            = {0}'.format(oDir)
    
    sDPP = symmetricDPPworker({'agentType' : agentType,
                               'm'         : m,
                               'method'    : 'iTsample',
                               'nSamples'  : nSamples,
                               'nAgents'   : nAgents})
    
    #initial uniform distribution
    tempDist = []
    p = float(1)/round(maxPrice - minPrice)
    a = [p]*(maxPrice - minPrice)
#    binEdges = [bin for bin in xrange( int(minPrice - maxPrice)+1 ) ]
    binEdges = numpy.arange(minPrice,maxPrice+1,1)
    for i in xrange(m):
        tempDist.append((numpy.atleast_1d(a),numpy.atleast_1d(binEdges)))
        
    currentDist = margDistSCPP(tempDist)
    
    #clean up
    # keep the binEdges for later histograms
    del p,a,tempDist
    
    ksList = []
    klList = []
    kappa = 1
    for t in xrange(0,L):
        print ""

        if verbose:
            print 'Iteration: {0}'.format(t)

        # set up the dampining constant if so specified
        if dampen:
            kappa = float(L-t)/L
            
        if verbose:
            print 'kappa = {0}'.format(kappa)
            gamesStart = time.clock()
            
        result = []
        
        if serial:
            # use serial 1 core implementation
            result = numpy.atleast_2d([r for r in itertools.imap(sDPP, itertools.repeat(currentDist,times=g))]).astype(numpy.float)
        else:
            pool = multiprocessing.Pool(processes=nProc)
            result = numpy.atleast_2d( pool.map(sDPP, itertools.repeat(currentDist,times=g)) ).astype(numpy.float)
            pool.close()
            pool.join()
            
        if verbose:
            gamesFinish = time.clock()
            print 'Finished {0} games in {1} seconds.'.format(g, gamesFinish-gamesStart)
            
        if verbose:
            histStart=time.clock() 
            
        histData = [] 
        histCount = []
        for m in xrange(result.shape[1]):
            histData.append(numpy.histogram(result[:,m],binEdges,density=True))
            histCount.append(numpy.histogram(result[:,m],binEdges,density=False))
            
        if verbose:
            histFinish = time.clock()
            print 'Histogramed {0} marginal distributions of {1} games {2} seconds'.\
                format(result.shape[1],g,histFinish-histStart)
                
        if verbose:
            updateStart = time.clock()
            
        
        updatedDist = updateDist(currDist = currentDist, 
                                 newDist = margDistSCPP(histData), 
                                 kappa = kappa, 
                                 verbose = verbose)
        
        if verbose:
            updateFinish = time.clock()
            print 'Updated distribution in {0} seconds.'.format(updateFinish-updateStart)
            
            
        ksList.append(ksStat(margDist1 = currentDist, margDist2 = updatedDist))
        klList.append(klDiv(currentDist, updatedDist))
        
        if pltItr:
            cs = cs = ['y--p', 'm-*', 'r-o','y-^','y-*']
            graphname = os.path.join(oDir,'ywSCPP_itr_{0}.png'.format(t))
            updatedDist.graphPdfToFile(fname = graphname,
                                       colorStyles = cs,
                                       title = "ywSCPP, {0}, kld = {1}, ks = {2}".format(agentType,klList[-1],ksList[-1]))
        
        if verbose:
            print 'Previous Expected Prices = {0}'.format(currentDist.expectedPrices())
            print 'New expected Prices      = {0}'.format(updatedDist.expectedPrices())
            print 'KS Statistic between Successive Iterations = {0}'.format(ksList[-1])
        
        if ksList[-1] <= d or t == (L-1):
            postfix = '{0}_{1}_{2}_{3}_{4}_{5}'.format(agentType, g, m, d,minPrice,maxPrice)
            pklName = 'distPricePrediction_' + postfix + '.pkl'
            txtName = 'distPricePrediction_' + postfix + '.txt'
            
            pricePredictionPklFilename = os.path.join(oDir, pklName) 
                                                      
            updatedDist.savePickle(pricePredictionPklFilename)
            
            pricePredictionTxtFilename = os.path.join(oDir, txtName)
            
            #this section could be improved....
            testdata = []
            for m in xrange(updatedDist.m):
                if m == 0:
                    textdata = numpy.vstack([updatedDist.data[m][0],updatedDist.data[m][1][:-1]])
                else:
                    textdata = numpy.vstack([textdata, numpy.vstack([updatedDist.data[m][0],updatedDist.data[m][1][:-1]])])
                    
            numpy.savetxt(pricePredictionTxtFilename,textdata)
            
            print ''
            print'Terminated after {0} Iterations'.format(t)
            print'Final Expected Price Vector = {0}'.format(updatedDist.expectedPrices())
            
            ksListName = os.path.join(oDir,'ksList.json')
            with open(ksListName,'w') as f:
                json.dump(ksList,f)
            klListName = os.path.join(oDir,'klList.json')
            with open(klListName,'w') as f:
                json.dump(klList,f)
            
            
            break
        else:
            currentDist = updatedDist
            del updatedDist
            
            
            
if __name__ == "__main__":
    ywSCPP(oDir = "C:/research/auction/ywTest2",
           g    = 1000)
           
        