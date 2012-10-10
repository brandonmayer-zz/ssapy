from ssapy.auctions import simulateAuction
from ssapy.pricePrediction.margDistSCPP import margDistSCPP
from ssapy.pricePrediction.util import klDiv, ksStat, updateDist

import numpy
import matplotlib.pyplot as plt

import os
import multiprocessing
import pickle
import glob
import copy
import time

def yw2Hob(**kwargs):
    oDir         = kwargs.get('oDir')
    if oDir == None:
        raise ValueError("Must specify oDir")
    if not os.path.exists(oDir):
        os.makedirs(oDir)
    
    agentType    = kwargs.get('agentType')
    if agentType == None:
        raise ValueError("Must specify agentType.")
    
    selfIdx      = kwargs.get('selfIdx',0)
    nAgents      = kwargs.get('nAgents',8)
    nGames       = kwargs.get('nGames',100)
    m            = kwargs.get('m',5)
    minPrice     = int(kwargs.get('minPrice',0))
    maxPrice     = int(kwargs.get('maxPrice',50))
    
    minValuation = kwargs.get('minValuation',0)
    maxValuation = kwargs.get('maxValuation',50)
    
    maxItr       = kwargs.get('maxItr', 100)
    tol          = kwargs.get('tol', 0.01)
    dampen       = kwargs.get('dampen', True)
    
    parallel     = kwargs.get('parallel',False)
    nProc        = kwargs.get('nProc',multiprocessing.cpu_count()-1)
    

    savePkl      = kwargs.get('savePkl',True)
    saveTime     = kwargs.get('saveTime',True)
    pltMarg      = kwargs.get('pltMarg',False)    
    pltKld       = kwargs.get('pltKld',True)
    pltKs        = kwargs.get('pltKs',True)
    verbose      = kwargs.get('verbose',True)
    
    if verbose:
        print 'oDir         = {0}'.format(oDir)
        print 'agentType    = {0}'.format(agentType)
        print 'nAgents      = {0}'.format(nAgents)
        print 'nGames       = {0}'.format(nGames)
        print 'm            = {0}'.format(m)
        print 'minPrice     = {0}'.format(minPrice)
        print 'maxPrice     = {0}'.format(maxPrice)
        print 'minValuation = {0}'.format(minValuation)
        print 'maxValuation = {0}'.format(maxValuation)
        print 'selfIdx      = {0}'.format(selfIdx)
        
        print 'maxItr       = {0}'.format(maxItr)
        print 'tol          = {0}'.format(tol)
        
        print 'parallel     = {0}'.format(parallel)
        print 'nProc        = {0}'.format(nProc)
    
        print 'savePkl      = {0}'.format(savePkl)
        print 'saveTime     = {0}'.format(saveTime)
        print 'pltMarg      = {0}'.format(pltMarg)
        print 'pltKld       = {0}'.format(pltKld)
        print 'pltKs        = {0}'.format(pltKs)
    
    if savePkl:
        pklDir = os.path.join(oDir, 'gmmPkl')
        if not os.path.exists(pklDir):
            os.makedirs(pklDir)
        else:
            [os.remove(f) for f in glob.glob(os.path.join(pklDir,'*.pkl'))]
            
    if pltMarg:
        margDir = os.path.join(oDir,'pltMarg')
        if not os.path.exists(margDir):
            os.makedirs(margDir)
        else:
            [os.remove(f) for f in glob.glob(os.path.join(margDir,'*.png'))]
            [os.remove(f) for f in glob.glob(os.path.join(margDir,'*.pdf'))]
            
    if saveTime:
        timeFile = os.path.join(oDir,'time.txt')
        if os.path.exists(timeFile):
            os.remove(timeFile)   
            
    klFile = os.path.join(oDir,'kld.txt')
    if os.path.exists(klFile):
        os.remove(klFile)
        
    ksFile = os.path.join(oDir,'ks.txt')
    if os.path.exists(ksFile):
        os.remove(ksFile)   
            
    #initial uniform distribution
    tempDist = []
    p = float(1)/round(maxPrice - minPrice)
    a = [p]*(maxPrice - minPrice)
    binEdges = numpy.arange(minPrice,maxPrice+1,1)
    for i in xrange(m):
        tempDist.append((numpy.atleast_1d(a),numpy.atleast_1d(binEdges)))
        
    currentDist = margDistSCPP(tempDist)
    
    del tempDist, p, a 
    
    if pltMarg:
        of = os.path.join(margDir,'yw2SccpHob_{0}_m{1}_n{2}_init.pdf'.format(agentType,m,nAgents))
        title = 'Marginal SCPP {0}'.format(agentType)
        xlabel = r'$q$'
        ylabel = r'$p(q)$'
        currentDist.graphPdfToFile(fname = of, title = title,  xlabel = xlabel, ylabel = ylabel)
        
    klList = []
    ksList = []
    for t in xrange(maxItr):
        if verbose:
            print ''
            print 'Iteration = {0}'.format(t)
            
        if dampen:
            kappa = numpy.float(maxItr - t) / maxItr
        else:
            kappa = 1
            
        if verbose:
            print 'kappa = {0}'.format(kappa)
            
        if verbose or saveTime:
            start = time.time()
            
        hob = simulateAuction( agentType       = agentType,
                               pricePrediction = currentDist,
                               m               = m,
                               nAgents         = nAgents,
                               nGames          = nGames,
                               parallel        = parallel,
                               nProc           = nProc,
                               minValuation    = minValuation,
                               maxValuation    = maxValuation,
                               retType         = 'hob',
                               selfIdx         = selfIdx,
                               verbose         = verbose)
        
        if verbose or saveTime:
            end = time.time()
            
        if verbose:
            print 'Simulated {0} auctions with {1} {2} agents in {3} seconds.'.format(nGames, nAgents, agentType, end-start)

        if savePkl:
            pklFile = os.path.join(pklDir, 'yw2ScppHob_{0}_m{1}_n{2}_{3:05d}.pkl'.format(agentType,m,nAgents,t))
            with open(pklFile,'wb') as f:
                pickle.dump(currentDist,f) 
                
        histData = []
        for goodIdx in xrange(hob.shape[1]):
            histData.append(numpy.histogram(hob[:,goodIdx],binEdges,density=True))
            
        newDist = margDistSCPP(histData)
        
        klList.append( klDiv(currentDist, newDist) )
        
        if verbose:
            print 'kld = {0}'.format(klList[-1])
            
        with open(klFile,'a') as f:
            f.write("{0}\n".format(klList[-1]))
        
        ksList.append( ksStat(currentDist,newDist) )
        
        if verbose:
            print 'kls = {0}'.format(ksList[-1])
            
        with open(ksFile,'a') as f:
            f.write("{0}\n".format(ksList[-1]))
        
        if saveTime:
            with open(timeFile,'a') as f:
                f.write("{0}\n".format(end-start))
                
        if pltMarg:
            of = os.path.join(margDir,'yw2SccpHob_{0}_m{1}_n{2}_{3:05d}.pdf'.format(agentType,m,nAgents,t))
            if verbose:
                print 'Plotting Marginal pdf to {0}'.format(of)
            title = 'Marginal SCPP {0}'.format(agentType)
            xlabel = r'$q$'
            ylabel = r'$p(q)$'
            newDist.graphPdfToFile(fname = of, title = title, xlabel = xlabel, ylabel = ylabel)
                
        if klList[-1] < tol or t == (maxItr - 1):
            
            if verbose:
                print 'kld = {0} < tol = {1}'.format(klList[-1],tol)
                
            if pltKld:
                
                if verbose:
                    print 'Plotting K-L Divergence vs. Iteration.'
                    
                klPdf = os.path.join(oDir,'kld.pdf')
                plt.figure()
                plt.plot(range(len(klList)), klList)
                plt.xlim((0,maxItr))
                plt.ylabel('K-L Divergence')
                plt.xlabel('Iteration')
                plt.title('Marginal SCPP {0}'.format(agentType))
                plt.savefig(klPdf)
                plt.close()
            
            if pltKs:
                
                if verbose:
                    print 'Plotting K-S Stat vs. Iteration'
                
                ksPdf = os.path.join(oDir,'ks.pdf')
                plt.figure()
                plt.plot(range(len(ksList)), ksList)
                plt.xlim((0,maxItr))
                plt.ylabel('K-S Statistic')
                plt.xlabel('Iteration')
                plt.title('Marginal SCPP {0}'.format(agentType))
                plt.savefig(ksPdf)
                plt.close()
                
            
            if verbose:
                print 'DONE!!!!!'
            
            break
        else:
            if verbose:
                print 'Updating distribution.'
            currentDist = updateDist(currentDist,newDist,kappa)
            del hob, newDist
              