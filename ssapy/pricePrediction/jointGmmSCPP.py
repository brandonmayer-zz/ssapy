import numpy
from sklearn import mixture
from ssapy.multiprocessingAdaptor import Consumer
from ssapy.agents.agentFactory import agentFactory
from ssapy.pricePrediction.margDistSCPP import margDistSCPP
from ssapy.pricePrediction.util import aicFit, drawGMM, \
    plotMargGMM, apprxJointGmmKL, simulateAuctionJointGMM

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.stats import norm

import json
import multiprocessing
import os 
import time
import random
import itertools
import argparse
import pickle
import glob

def jointGaussSCPP(**kwargs):
    oDir = kwargs.get('oDir')
    if not oDir:
        raise ValueError("Must provide output Directory")
    oDir = os.path.realpath(oDir)
    
    agentType    = kwargs.get('agentType',"straightMV")
    nAgents      = kwargs.get('nAgnets',8)
    nGames       = kwargs.get('nGames',10)
    nSamples     = kwargs.get('nSamples',8)
    m            = kwargs.get('m',5)
    minPrice     = kwargs.get('minPrice',0)
    maxPrice     = kwargs.get('maxPrice',50)
    serial       = kwargs.get('serial',False)
    klSamples    = kwargs.get('klSamples',1000)
    maxItr       = kwargs.get('maxItr', 100)
    tol          = kwargs.get('tol', 0.01)
    pltDist      = kwargs.get('pltDist',True)
    nProc        = kwargs.get('nProc',multiprocessing.cpu_count()-1)
    minCovar     = kwargs.get('minCovar',9)
    covarType    = kwargs.get('covarType','full')
    savePkl      = kwargs.get('savePkl',True)
    verbose      = kwargs.get('verbose',True) 
    aicCompMin   = kwargs.get('aicCompMin',1)
    aicCompMax   = kwargs.get('aicCompMax',10)
    aicMinCovar  = kwargs.get('aicMinCovar',9)
    plotMarginal = kwargs.get('pltMarg',True)
    
    if verbose:
        print 'agentType  = {0}'.format(agentType)
        print 'nAgents     = {0}'.format(nAgents)
        print 'nGames      = {0}'.format(nGames)
        print 'm           = {0}'.format(m)
        print 'minPrice    = {0}'.format(minPrice)
        print 'maxPrice    = {0}'.format(maxPrice)
        print 'maxItr      = {0}'.format(maxItr)
        print 'tol         = {0}'.format(tol)
        print 'klSamples   = {0}'.format(klSamples)
        print 'pltDist     = {0}'.format(pltDist)
        print 'serial      = {0}'.format(serial)
        print 'nProc       = {0}'.format(nProc)
        print 'minCovar    = {0}'.format(minCovar)
        print 'aicCompMin  = {0}'.format(aicCompMin)
        print 'aicCompMax  = {0}'.format(aicCompMax)
        print 'aicMinCovar = {0}'.format(aicMinCovar)
        
        
    
    if savePkl:
        pklDir = os.path.join(oDir, 'gmmPkl')
        if not os.path.exists(pklDir):
            os.makedirs(pklDir)
            
    if pltDist:
        pltDir = os.path.join(oDir,'gmmPlts')
        if not os.path.exists(pltDir):
            os.makedirs(pltDir)
        else:
            [os.remove(f) for f in glob.glob(os.path.join(pltDir,'*.png'))]
        histDir = os.path.join(oDir,'gmmHist')
        
        if not os.path.exists(histDir):
            os.makedirs(histDir)
            
    if pltMarg:
        margDir = os.path.join(oDir,'pltMarg')
        if not os.path.exists(pltDir):
            os.makedirs(pltDir)
        else:
            [os.remove(f) for f in glob.glob(os.path.join(pltMarg,'*.png'))]
        
        
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
        
        clfCurr, aicList, compRange = aicFit(winningBids,
                                             compRange = range(aicCompMin,aicCompMax), 
                                             minCovar = aicMinCovar)    
        
        if savePkl:
            pklFile = os.path.join(pklDir,'gmm_{0}.pkl'.format(itr))
            with open(pklFile,'wb') as f:
                pickle.dump(clfCurr, f)
        
        if clfPrev:
            kl = apprxJointGmmKL(clfCurr, clfPrev, klSamples)
            klList.append(kl)
            if verbose:
                print 'kl = {0}'.format(kl) 
                
        
            
        if pltDist:
            if m == 2:
                if verbose:
                    print 'plotting joint distribution'
            
                oFile = os.path.join(pltDir, 'jointGmmSCPP_{0}.png'.format(itr))
                if klList: 
                    title = "jointGmmSCPP itr = {0} kld = {1}".format(itr,klList[-1])
                else:
                    title = "jointGmmSCPP itr = {0}".format(itr)
                f = plt.figure()
                ax = f.add_subplot(111,projection='3d')
                ax.view_init(26,-142)
                
                X = numpy.arange(minPrice,maxPrice,0.25)
                Y = numpy.arange(minPrice,maxPrice,0.25)
                xx,yy = numpy.meshgrid(X, Y)
                s = numpy.transpose(numpy.atleast_2d([xx.ravel(),yy.ravel()]))

                Z = numpy.exp(clfCurr.eval(s)[0].reshape(xx.shape))
                
                surf = ax.plot_surface(xx, yy, Z, rstride=1, cstride=1, cmap=cm.jet,
                                       linewidth=0, antialiased=True)
                            
#                f.colorbar(surf,shrink=0.5,aspect=5)
                
                nComp = clfCurr.means_.shape[0]
                ax.set_title("nComp = {0}".format(nComp))
                
                plt.savefig(oFile)
                
                of2 = os.path.join(histDir,'gaussJointHistSCPP_{0}.png'.format(itr))
                H, xedges, yedges = numpy.histogram2d(winningBids[:,0], winningBids[:,1], bins = numpy.arange(minPrice,maxPrice+1),normed=True)
                extent = [yedges[0], yedges[-1], xedges[0], xedges[-1]]
                plt.figure()
                plt.imshow(H,extent=extent,interpolation='nearest',origin='lower')
                plt.colorbar()
                
                plt.savefig(of2)
                
            if pltMarg:
                if verbose:
                    print 'plotting marginal distribution'
                nComp = clf.means_.shape[0]
                
                for goodIdx in xrange(m):
                    x = numpy.linspace(minPrice,maxPrice,10000)
                    
                    for (w,m,c) in zip(clf.weights_,clf.means_,clf.covars_):
                        pass
                    
                
        if klList:
            if numpy.abs(klList[-1]) < tol:
                break
                
        clfPrev = clfCurr
        
    if klList: 
        klFile = os.path.join(oDir,'kld.json')
        with open(klFile,'w') as f:
            json.dump(klList,f)
                    
        print 'kld = {0} < tol = {1}'.format(klList[-1],tol)
        print 'DONE'
        
    
    
    
     