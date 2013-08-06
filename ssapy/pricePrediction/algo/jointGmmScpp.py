import matplotlib
matplotlib.use('Agg',warn=False)

import matplotlib.pyplot as plt

import argparse

import numpy
import multiprocessing
import os
import sys
import json
import time
import pickle

from ssapy import timestamp_
from ssapy.auctions import simulateAuction
from ssapy.pricePrediction import uniformpp
from ssapy.pricePrediction.jointGMM import jointGMM
from ssapy.util.padnums import pprint_table
from ssapy.pricePrediction.util import apprxJointGmmKL

def paramString(**kwargs):
    ss = 'gmmScpp_{0}_{1:03}_{2:03}_{3}_{4:04}_{5:04}_{6}_{7}_{8}_{9}_{10}_{11}_{12}_{13}'.\
            format(kwargs['agentType'], kwargs['m'],kwargs['nAgents'],kwargs['covariance_type'], 
            kwargs['nGames'], kwargs['maxItr'], kwargs['tol'], kwargs['aicMinCovar'],
            kwargs['aicCompMin'], kwargs['aicCompMax'], kwargs['minValuation'], 
            kwargs['maxValuation'], kwargs['l'], kwargs['timeStamp'])
    
    return ss

def fileNamePostfix(**kwargs):
    ss = r'{0}_{1:03}_{2:03}_{3}'.\
        format(kwargs['agentType'],kwargs['m'],kwargs['nAgents'],kwargs['l'],kwargs['timeStamp'])
        
    return ss

def outputDir(**kwargs):
    ss = paramString(**kwargs)
    
    ss = ss + '_' + timestamp_()
    
    oDir = os.path.join(kwargs['oDir'],ss)
    if not os.path.exists(oDir):
        os.makedirs(oDir)
        
    return oDir

def pltAic(compRange, aicValues, itr, filename):
    f,ax = plt.subplots()
    colors = ['#777777']*len(aicValues)
    colors[numpy.argmin(aicValues)] = 'r'
    ax.bar(compRange, aicValues, color=colors, align = 'center')
    ax.set_ylabel('AIC score')
    ax.set_xlabel('GMM Model (Number of Components)')
    ax.set_title('Iteration {0}'.format(itr+1))
    plt.ylim([0,numpy.max(aicValues) + 0.5])
    plt.savefig(filename)

def jointGmmScpp(**kwargs):
    """
    NOTE: EXTRA MODEL IS FIT TO FULL COVAR GMM - regardless of
    covariance_type kwarg.
    """
    
    kwargs['oDir']         = kwargs.get('oDir')
    if kwargs['oDir'] == None:
        raise ValueError("Must specify output directory - oDir.")
    
    kwargs['agentType']    = kwargs.get('agentType')
    
    if kwargs['agentType'] == None:
        raise ValueError('Must specify agent type - agentType.')
    kwargs['nAgents']      = kwargs.get('nAgents',5)

    kwargs['selfIdx']      = kwargs.get('selfIdx',numpy.random.randint(kwargs['nAgents']))
    
    kwargs['nGames']       = kwargs.get('nGames',10000)
    kwargs['nklsamples']   = kwargs.get('nklsamples',1000)
    
    kwargs['maxItr']       = kwargs.get('maxItr',100)

    kwargs['tol']          = kwargs.get('tol',0.01)
    
    kwargs['aicCompMin']   = kwargs.get('aicCompMin',5)

    kwargs['aicCompMax']   = kwargs.get('aicCompMax',21)

    kwargs['aicMinCovar']  = kwargs.get('aicMinCovar',0.1)

    kwargs['minPrice']     = kwargs.get('minPrice',0)
    
    kwargs['maxPrice']     = kwargs.get('maxPrice',numpy.float('inf'))
    
    kwargs['covariance_type']   = kwargs.get('covariance_type','full')
    
    kwargs['m']            = kwargs.get('m',5)

    kwargs['minValuation'] = kwargs.get('vmin',0)
    kwargs['maxValuation'] = kwargs.get('vmax',50)

    kwargs['parallel']     = kwargs.get('parallel',True)
    
    kwargs['nProc']        = kwargs.get('nProc', multiprocessing.cpu_count())
    
    kwargs['verbose']      = kwargs.get('verbose', True)
    
    kwargs['pltMarg']      = kwargs.get('pltMarg', True)
    
    kwargs['l']            = kwargs.get('l')
    
    kwargs['timeStamp']    = timestamp_()

    ps = paramString(**kwargs)
            
    kwargs['oDir'] = os.path.join(kwargs['oDir'],ps)
    if not os.path.exists(kwargs['oDir']):
        os.makedirs(kwargs['oDir'])
    
    models = numpy.arange(kwargs['aicCompMin'], kwargs['aicCompMax'])
            
    if kwargs['verbose']:    
        table = []
        
        for k,v in kwargs.iteritems():
            table.append([k,str(v)])
        
        pprint_table(sys.stdout, table)
    
    with open(os.path.join(kwargs['oDir'],'params.txt'),'w') as f:
        pprint_table(f, table)
        
    with open(os.path.join(kwargs['oDir'],'params.json'),'w') as f:
        json.dump(kwargs, f)
        
    kwargs['pricePrediction'] = uniformpp(kwargs['m'],kwargs['minValuation'],kwargs['maxValuation'])
    
    idx2keep = numpy.arange(kwargs['nAgents'])
    idx2keep = numpy.delete(idx2keep, kwargs['selfIdx'])
    if kwargs['verbose']:
        print 'indicies to keep = {0}'.format(idx2keep)
    
    filePostfix = fileNamePostfix(**kwargs)
    
    
    for itr in xrange(kwargs['maxItr']):
        itrStart = time.time()
        if kwargs['verbose']:
            print 'Iteration {0}'.format(itr+1)
        
        simStart = time.time()
        bids = simulateAuction(**kwargs)
        simEnd = time.time()
#        simFile = os.path.realpath(os.path.join(kwargs['oDir'],"simulationTime_{0}.txt".format(ps)))
        simFile = os.path.join(kwargs['oDir'],'simTime_0.01.txt')
#        if not simFile:
#            with open(os.path.realpath(simFile),'w+') as f:
#                numpy.savetxt(f, numpy.atleast_1d(simEnd-simStart))
#        else:
#        with open(os.path.join(kwargs['oDir'],"simulationTime_{0}.txt".format(ps)),'a+') as f:
        with open(simFile,'a+') as f:
            numpy.savetxt(f, numpy.atleast_1d(simEnd-simStart)) 
            
        if kwargs['verbose']:
            print 'Simulated {0} auctions in {1} seconds'.format(kwargs['nGames'],simEnd-simStart)
            
        del simStart, simEnd
        
        bidsFile = 'bids_{0:04}_{1}.npy'.format(itr,filePostfix)
        with open(os.path.join(kwargs['oDir'], bidsFile),'w') as f:
            numpy.save(f, bids)
            
        hob = numpy.max(bids[:,idx2keep,:],1)
        hobFile = os.path.join(kwargs['oDir'],'hob_{0:04}_{1}.txt'.format(itr,filePostfix))
        with open(hobFile,'w') as f:
            numpy.savetxt(f,hob)
        
        del bids
                    
        nextpp = jointGMM(covariance_type = kwargs.get('covariance_type'))
        temppp, aicValues, compRange = nextpp.aicFit(X=hob, compRange = models, min_covar = kwargs['aicMinCovar'], verbose = kwargs['verbose'])
        
        aicFile = os.path.join(kwargs['oDir'],'aic_{0:03}_{1}.pdf'.format(itr+1,filePostfix))
        
        pltAic(compRange,aicValues,itr,aicFile)
        
        del hob,temppp,compRange
        
        ppFile = os.path.join(kwargs['oDir'], 'gmmScpp_{0:04}_{1}.pkl'.format(itr,filePostfix))
        with open(ppFile,'w') as f:
            pickle.dump(nextpp,f)
            
        if kwargs['pltMarg']:
            oFile = os.path.join(kwargs['oDir'],'marg_{0:04}_{1}.pdf'.format(itr,filePostfix))
            nextpp.pltMarg(oFile = oFile)
        
        with open(os.path.join(kwargs['oDir'],'aic_{0:04}_{1}.txt'.format(itr,filePostfix)),'a') as f:
            numpy.savetxt(f,numpy.atleast_1d(aicValues).T)
        
        if kwargs['verbose']:
            print 'AIC Fit: number of components = {0}'.format(nextpp.n_components)
            
        with open(os.path.join(kwargs['oDir'],'n_components_{0}.txt'.format(filePostfix)), 'a') as f:
            numpy.savetxt(f,numpy.atleast_1d(nextpp.n_components))
            
        if itr > 0:
            kld = numpy.abs(apprxJointGmmKL(kwargs['pricePrediction'], nextpp, 
                            nSamples = kwargs['nklsamples'], verbose = kwargs['verbose']))
            
            with open(os.path.join(kwargs['oDir'],'kld_{0}.txt'.format(filePostfix)),'a') as f:
                numpy.savetxt(f,numpy.atleast_1d(kld))
                
            if kwargs['verbose']:
                print 'Symmetric KL Distance = {0}'.format(kld)
        
        itrEnd = time.time()
        with open(os.path.join(kwargs['oDir'], "itrTime_{0}.txt".format(filePostfix)),'a') as f:
            numpy.savetxt(f, numpy.atleast_1d(itrEnd-itrStart))
            
        kwargs['pricePrediction'] = nextpp
        
        if itr > 0:
            if kld < kwargs['tol']:
                if kwargs['verbose']:
                    print 'kld = {0} < tol = {1}'.format(kld, kwargs['tol'])
                    print 'CONVERGED!'
                    
                break
        else:
            print ''
            
    with open(os.path.join(kwargs['oDir'],'kld_{0}.txt'.format(filePostfix)),'r') as f:
        kld = numpy.loadtxt(f, 'float')
     
    f, ax = plt.subplots()
    plt.plot(kld,'r-',linewidth=3)
    plt.title("Absolute Symmetric K-L Divergence")
    plt.xlabel("Iteration")
    plt.ylabel(r"|kld|")
    plt.savefig(os.path.join(kwargs['oDir'],'kld_{0}.pdf'.format(ps)))
    
    del kld
    
    with open(os.path.join(kwargs['oDir'],'n_components_{0}.txt'.format(filePostfix)),'r') as f:
        comp = numpy.loadtxt(f)
        
    f,ax = plt.subplots()
    colors = ['#0A0A2A']*len(aicValues)
    ax.bar(range(len(comp)), comp, color=colors, align = 'center')
    ax.set_ylabel('GMM Model (Number of Components)')
    ax.set_xlabel('Iteration')
    ax.set_title('Model Selection')
    plt.ylim([0,numpy.max(comp) + 0.5])
    plt.savefig(os.path.join(kwargs['oDir'],'n_components_{0}.pdf'.format(ps)))
    
    del comp
    
    if kwargs['verbose']:
        print 'Simulating {0} auctions after scpp converged.'.format(kwargs['nGames'])
    
    # To check if distribution is SCPP, after convergence simulate
    # more bids then evaluate measures of similarity between the resulting 
    # bids and the scpp candidate.
    start = time.time()    
    extraBids = simulateAuction(**kwargs)
    end = time.time()
    
    with open(os.path.join(kwargs['oDir'],'extraBids_{0}.npy'.format(filePostfix)), 'w') as f:
        numpy.save(f, extraBids)
    
    if kwargs['verbose']:
        print 'Simulated {0} holdout auctions in {1} seconds'.format(kwargs['nGames'],end-start)
        
    extraHob = numpy.max(extraBids[:,idx2keep,:],1)
    with open(os.path.join(kwargs['oDir'],'extraHob_{0}.txt'.format(filePostfix)),'w') as f:
        numpy.savetxt(f, extraHob)
    
    ll = numpy.sum(kwargs['pricePrediction'].eval(extraHob)[0])
    
    if kwargs['verbose']:
        print 'log-likelihood hold out = {0}'.format(ll)
        
    with open(os.path.join(kwargs['oDir'],'extraHobLL_{0}.txt'.format(filePostfix)),'w') as f:
        numpy.savetxt(f,numpy.atleast_1d(ll))
        
    # fit another model to held out data and
    # compute the last skl between the scpp and 
    # the extra model
    
    extraModel = jointGMM()
    gmm, aicValues, compRange = extraModel.aicFit(X=extraHob, compRange = models, min_covar = kwargs['aicMinCovar'], verbose = kwargs['verbose'])
    kld = numpy.abs(apprxJointGmmKL(kwargs['pricePrediction'], extraModel, nSamples = kwargs['nklsamples'], verbose = kwargs['verbose']))
    
    f,ax = plt.subplots()
    colors = ['#777777']*len(aicValues)
    colors[numpy.argmin(aicValues)] = 'r'
    ax.bar(compRange, aicValues, color=colors, align = 'center')
    ax.set_ylabel('AIC score')
    ax.set_xlabel('GMM Model (Number of Components)')
    ax.set_title('Iteration {0}'.format(itr+1))
    plt.ylim([0,numpy.max(aicValues) + 0.5])
    extraAicFile = "extraAic_{0:04}_{1}.pdf".format(itr+1,ps)
    plt.savefig(os.path.join(kwargs['oDir'],extraAicFile))
    
    del gmm,aicValues, compRange
    
    if kwargs['verbose']:
        print 'SKL-D between SCPP proposal and extra model = {0}'.format(kld)
        
    extraSkdFile = os.path.join(kwargs['oDir'],'extraHobSkl_{0}.txt'.format(filePostfix))
    with open(extraSkdFile,'w') as f:
        numpy.savetxt(f, numpy.atleast_1d(kld))