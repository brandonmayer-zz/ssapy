from ssapy.agents.agentFactory import agentFactory
from ssapy.auctions import simulateAuction
from ssapy.pricePrediction.margDistSCPP import margDistSCPP
from ssapy.pricePrediction.jointGMM import jointGMM
from ssapy.pricePrediction.util import apprxJointGmmKL


import numpy

import os
import multiprocessing
import pickle
import glob
import copy

def jointGaussScppHob(**kwargs):
    oDir         = kwargs.get('oDir')
    agentType    = kwargs.get('agentType',"straightMV")
    selfIdx      = kwargs.get('selfIdx',0)
    nAgents      = kwargs.get('nAgents',8)
    nGames       = kwargs.get('nGames',100)
    m            = kwargs.get('m',5)
    minPrice     = kwargs.get('minPrice',0.0)
    maxPrice     = kwargs.get('maxPrice',numpy.float('inf'))
    minValuation = kwargs.get('minValuation',0)
    maxValuation = kwargs.get('maxValuation',50)
    
    parallel     = kwargs.get('parallel',False)
    nProc        = kwargs.get('nProc',multiprocessing.cpu_count()-1)
    
    klSamples    = kwargs.get('klSamples',10000)
    
    covarType    = kwargs.get('covarType','full')
    aicCompMin   = kwargs.get('aicCompMin',1)
    aicCompMax   = kwargs.get('aicCompMax',10)
    aicMinCovar  = kwargs.get('aicMinCovar',1.0)
    
    maxItr       = kwargs.get('maxItr', 100)
    tol          = kwargs.get('tol', 0.01)
    
    savePkl      = kwargs.get('savePkl',True)
    verbose      = kwargs.get('verbose',True)
    
    pltSurf      = kwargs.get('pltSurf',False)
    pltMarg      = kwargs.get('pltMarg',False)
    
    if oDir is None:
        raise ValueError("Must provide output Directory")
    oDir = os.path.realpath(oDir)
    
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
        
        print 'parallel     = {0}'.format(parallel)
        print 'nProc        = {0}'.format(nProc)
        
        print 'klSamples    = {0}'.format(klSamples)
        
        print 'aicCompMin   = {0}'.format(aicCompMin)
        print 'aicCompMax   = {0}'.format(aicCompMax)
        print 'aicMinCovar  = {0}'.format(aicMinCovar)
        
        print 'maxItr       = {0}'.format(maxItr)
        print 'tol          = {0}'.format(tol)
        
        print 'savePkl      = {0}'.format(savePkl)
        print 'pltSurf      = {0}'.format(pltSurf)
        print 'pltMarg      = {0}'.format(pltMarg)
        
        if savePkl:
            pklDir = os.path.join(oDir, 'gmmPkl')
        if not os.path.exists(pklDir):
            os.makedirs(pklDir)
        else:
            [os.remove(f) for f in glob.glob(os.path.join(pklDir,'*.pkl'))]
            
        if pltSurf:
            pltDir = os.path.join(oDir,'pltSurf')
        if not os.path.exists(pltDir):
            os.makedirs(pltDir)
        else:
            [os.remove(f) for f in glob.glob(os.path.join(pltDir,'*.png'))]
            
        if pltMarg:
            margDir = os.path.join(oDir,'pltMarg')
        if not os.path.exists(margDir):
            os.makedirs(margDir)
        else:
            [os.remove(f) for f in glob.glob(os.path.join(margDir,'*.png'))]
    
        clfCurr = jointGMM(minPrice = minPrice, maxPrice = maxPrice)
        clfPrev = None
        klList = []
        
        for itr in xrange(maxItr):
            print ''
            print 'Iteration = {0}'.format(itr)
            
            if itr == 0:
                tempDist = []
                p = float(1)/50
                a = [p]*50
                binEdges = numpy.arange(0,51,1)
                for i in xrange(m):
                    tempDist.append((numpy.atleast_1d(a),numpy.atleast_1d(binEdges)))
                    
                pricePrediction = margDistSCPP(tempDist)
            else:
                pricePrediction = clfCurr
            
            hob = simulateAuction( agentType       = agentType,
                                   pricePrediction = pricePrediction,
                                   nAgents         = nAgents,
                                   nGames          = nGames,
                                   parallel        = parallel,
                                   nProc           = nProc,
                                   m               = m,
                                   minValuation    = minValuation,
                                   maxValuation    = maxValuation,
                                   retType         = 'hob',
                                   selfIdx         = selfIdx,
                                   verbose         = verbose )
            
            clfCurr.aicFit(X = hob, 
                           compRange = range(aicCompMin, aicCompMax),
                           covariance_type = covarType, 
                           min_covar = aicMinCovar, 
                           verbose = verbose)
            
            if savePkl:
                pklFile = os.path.join(pklDir,'jointGmmScppHob_{0}_m{1}_n{2}_{3:05d}.pkl'.format(agentType,m,nAgents,itr))
                with open(pklFile,'wb') as f:
                    pickle.dump(clfCurr, f)
                
            if clfPrev:
                kl = apprxJointGmmKL(clfCurr, clfPrev, klSamples)
                klList.append(kl)
                if verbose:
                    print '|kl| = {0}'.format(numpy.abs(kl)) 
                    
            if pltSurf:
                of = os.path.join(pltDir, 'jointGmmScppHobSurf_{0}_m{1}_n{2}_{3:05d}.png'.format(agentType,m,nAgents,itr))
                
                if verbose:
                    print 'plotting joint distribution surface.'
                
                title = 'Joint Gmm SCPP {0}\n Iteration: {1}'.format(agentType, itr)
                clfCurr.plt(oFile = of, title = title)  
                
            if pltMarg:
            
                of = os.path.join(margDir,'jointGmmScppHobMarg_{0}_m{1}_n{2}_{3:05d}.png'.format(agentType,m,nAgents,itr))
                
                if verbose:
                    print 'plotting marginal distribution'
                
                if itr > 0:
                    title = "Marginal Distribution of Joint {0}\n itr = {1}, |kld| = {2}".format(agentType,itr,numpy.abs(kl))
                else:
                    title = "Marginal Distribution of Joint {0}\n itr = {1}".format(agentType,itr)
                
                clfCurr.pltMargDist(oFile = of, title = title, ylabel = r'$p(q)$', xlabel = r'$q$')
                                       
            if klList:
                print klList
                if numpy.abs(klList[-1]) < tol:
                    break
                
            clfPrev = copy.deepcopy(clfCurr)
            
        if klList:
            klFile = os.path.join(oDir,'kld.txt')
            numpy.savetxt(klFile, numpy.asarray(klList))
            
            if verbose:
                
                print '|kld| = {0} < tol = {1}'.format(numpy.abs(klList[-1]),tol)
                print 'DONE - Iteration = {0}'.format(itr)
