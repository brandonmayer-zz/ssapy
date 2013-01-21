import numpy
import multiprocessing
import os
import sys
import json
import time
import pickle
import matplotlib.pyplot as plt

from ssapy import timestamp_
from ssapy.auctions import simulateAuction
from ssapy.pricePrediction import uniformpp
from ssapy.pricePrediction.jointGMM import jointGMM
from ssapy.util.padnums import pprint_table
from ssapy.pricePrediction.util import apprxJointGmmKL

def jointGmmScppHob(**kwargs):
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
    
    kwargs['m']            = kwargs.get('m',5)

    kwargs['minValuation'] = kwargs.get('vmin',0)
    kwargs['maxValuation'] = kwargs.get('vmax',50)

    kwargs['parallel']     = kwargs.get('parallel',True)
    kwargs['nProc']        = kwargs.get('nProc', multiprocessing.cpu_count())
    kwargs['verbose']      = kwargs.get('verbose', True)
    kwargs['pltMarg']      = kwargs.get('pltMarg', True)
    
    kwargs['misamples']    = kwargs.get('misamples', 10000)
    
    if kwargs['oDir'] == None:
        raise ValueError("Must provide Directory")
    kwargs['oDir'] = os.path.realpath(kwargs['oDir'])
    
    models = numpy.arange(kwargs['aicCompMin'], kwargs['aicCompMax'])
        
    timestamp = "jointGmmScpp_{0}_{1}".format(kwargs['agentType'],timestamp_())
    
    kwargs['oDir'] = os.path.join(kwargs['oDir'], timestamp)
    if not os.path.exists(kwargs['oDir']):
        os.makedirs(kwargs['oDir'])
    
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
        print idx2keep
    
    for itr in xrange(kwargs['maxItr']):
        itrStart = time.time()
        if kwargs['verbose']:
            print 'Iteration {0}'.format(itr+1)
        
        simStart = time.time()
        bids = simulateAuction(**kwargs)
        simEnd = time.time()
        with open(os.path.join(kwargs['oDir'],"simulationTime.txt"),'a') as f:
            numpy.savetxt(f, numpy.atleast_1d(simEnd-simStart)) 
            
        if kwargs['verbose']:
            print 'Simulated {0} auctions in {1} seconds'.format(kwargs['nGames'],simEnd-simStart)
            
        del simStart, simEnd
        
        bidsFile = 'bids_{0:04}.npy'.format(itr)
        with open(os.path.join(kwargs['oDir'], bidsFile),'w') as f:
            numpy.save(f, bids)
            
        hob = numpy.max(bids[:,idx2keep,:],1)
        hobFile = os.path.join(kwargs['oDir'],'hob_{0:04}.txt'.format(itr))
        with open(hobFile,'w') as f:
            numpy.savetxt(f,hob)
        
        del bids
                    
        nextpp = jointGMM()
        temppp, aicValues, compRange = nextpp.aicFit(X=hob, compRange = models, min_covar = kwargs['aicMinCovar'], verbose = kwargs['verbose'])
        
        f,ax = plt.subplots()
        colors = ['#777777']*len(aicValues)
        colors[numpy.argmin(aicValues)] = 'r'
        ax.bar(compRange, aicValues, color=colors, align = 'center')
        ax.set_ylabel('AIC score')
        ax.set_xlabel('GMM Model (Number of Components)')
        ax.set_title('Iteration {0}'.format(itr+1))
        plt.ylim([0,numpy.max(aicValues) + 0.5])
        aicFile = "aic_{0:03}.pdf".format(itr+1)
        plt.savefig(os.path.join(kwargs['oDir'],aicFile))
        del colors
        
        del hob,temppp,compRange
        
        ppFile = os.path.join(kwargs['oDir'], 'jointGmmScppHob_{0}_{1:04}.pkl'.format(kwargs['agentType'],itr+1))
        with open(ppFile,'w') as f:
            pickle.dump(nextpp,f)
            
        if kwargs['pltMarg']:
            oFile = os.path.join(kwargs['oDir'],'jointGmmScppHob_{0}_m_{1}_{2:04}.pdf'.format(kwargs['agentType'],kwargs['m'],itr+1))
            nextpp.pltMarg(oFile = oFile)
        
        with open(os.path.join(kwargs['oDir'],'aic.txt'),'a') as f:
            numpy.savetxt(f,numpy.atleast_1d(aicValues))
        
        if kwargs['verbose']:
            print 'AIC Fit: number of components = {0}'.format(nextpp.n_components)
            
        with open(os.path.join(kwargs['oDir'],'n_components.txt'), 'a') as f:
            numpy.savetxt(f,numpy.atleast_1d(nextpp.n_components))
            
        if itr > 0:
            kld = numpy.abs(apprxJointGmmKL(kwargs['pricePrediction'], nextpp, nSamples = kwargs['nklsamples'], verbose = kwargs['verbose']))
            
            with open(os.path.join(kwargs['oDir'],'kld.txt'),'a') as f:
                numpy.savetxt(f,numpy.atleast_1d(kld))
                
            if kwargs['verbose']:
                print 'Symmetric KL Distance = {0}'.format(kld)
        
        itrEnd = time.time()
        with open(os.path.join(kwargs['oDir'], "itrTime.txt"),'a') as f:
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
            
    with open(os.path.join(kwargs['oDir'],'kld.txt'),'r') as f:
        kld = numpy.loadtxt(f, 'float')
     
    f, ax = plt.subplots()
    plt.plot(kld,'r-',linewidth=3)
    plt.title("Absolute Symmetric K-L Divergence")
    plt.xlabel("Iteration")
    plt.ylabel(r"|kld|")
    plt.savefig(os.path.join(kwargs['oDir'],'kld.pdf'))
    
    del kld
    
    with open(os.path.join(kwargs['oDir'],'n_components.txt'),'r') as f:
        comp = numpy.loadtxt(f)
        
    f,ax = plt.subplots()
    colors = ['#0A0A2A']*len(aicValues)
    colors[numpy.argmin(aicValues)] = 'r'
    ax.bar(range(len(comp)), comp, color=colors, align = 'center')
    ax.set_ylabel('GMM Model (Number of Components)')
    ax.set_xlabel('Iteration')
    ax.set_title('Model Selection')
    plt.ylim([0,numpy.max(comp) + 0.5])
    plt.savefig(os.path.join(kwargs['oDir'],'n_components.pdf'))
    
    del comp
    
    if kwargs['verbose']:
        print 'Simulating {0} auctions after scpp converged.'.format(kwargs['nGames'])
    
    # To check if distribution is SCPP, after convergence simulate
    # more bids then evaluate measures of similarity between the resulting 
    # bids and the scpp candidate.
    start = time.time()    
    extraBids = simulateAuction(**kwargs)
    end = time.time()
    
    with open(os.path.join(kwargs['oDir'],'extraBids.npy'), 'w') as f:
        numpy.save(f, extraBids)
    
    if kwargs['verbose']:
        print 'Simulated {0} holdout auctions in {1} seconds'.format(kwargs['nGames'],end-start)
        
    extraHob = numpy.max(extraBids[:,idx2keep,:],1)
    with open(os.path.join(kwargs['oDir'],'extraHob.txt'),'w') as f:
        numpy.savetxt(f, extraHob)
    
    ll = numpy.sum(kwargs['pricePrediction'].eval(extraHob)[0])
    
    if kwargs['verbose']:
        print 'log-likelihood hold out = {0}'.format(ll)
        
    with open(os.path.join(kwargs['oDir'],'extraHobLL.txt'),'w') as f:
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
    extraAicFile = "extraAic_{0:03}.pdf".format(itr+1)
    plt.savefig(os.path.join(kwargs['oDir'],extraAicFile))
    
    del gmm,aicValues, compRange
    
    if kwargs['verbose']:
        print 'SKL-D between SCPP proposal and extra model = {0}'.format(kld)
        
    extraSkdFile = os.path.join(kwargs['oDir'],'extraHobSkl.txt')
    with open(extraSkdFile,'w') as f:
        numpy.savetxt(f, numpy.atleast_1d(kld))
        
    mi = nextpp.mutualInformation(kwargs['misamples'])
    
    with open(os.path.join(kwargs['oDir'], mi.txt),'w') as f:
        print >> f, "{0}".format(mi)
    
if __name__ == "__main__":
    oDir = os.path.realpath("C:/Users/bm/Desktop/testdir")
    jointGmmScppHob(oDir=oDir, m = 2, maxItr = 5, nGames = 100, parallel=True, agentType = 'msStraightMUa')