from ssapy.agents.agentFactory import agentFactory

import multiprocessing
import numpy

def simulateAuction(**kwargs):

    agentType = kwargs.get('agentType')
        
    if isinstance(agentType,list):
        nAgents = len(agentType)
    elif isinstance(agentType,str):
        nAgents   = kwargs.get('nAgents',8)
        agentType = [agentType]*nAgents
    
    nGames          = kwargs.get('nGames')
    parallel        = kwargs.get('parallel',True)
    nProc           = kwargs.get('nProc', multiprocessing.cpu_count())
    pricePrediction = kwargs.get('pricePrediction')
        
    m            = kwargs.get('m',5)
    minValuation = kwargs.get('minValuation',0)
    maxValuation = kwargs.get('maxValuation',50)
    minPrice     = kwargs.get('minPrice',0)
    maxPrice     = kwargs.get('maxPrice',numpy.float('inf'))
    
    verbose      = kwargs.get('verbose', False)
    
    if verbose:
        print 'In simulateAuction(...)'
        print 'agentType    = {0}'.format(agentType)
        print 'nGames       = {0}'.format(nGames)
        print 'parallel     = {0}'.format(parallel)
        print 'nProc        = {0}'.format(nProc)
        print 'm            = {0}'.format(m)
        print 'minValuation = {0}'.format(minValuation)
        print 'maxValuation = {0}'.format(maxValuation)
        print 'minPrice     = {0}'.format(minPrice)
        print 'maxPrice     = {0}'.format(maxPrice)
    
    bids = numpy.zeros((nGames*nAgents,m))
    
    if parallel:
        pool = multiprocessing.Pool(nProc)
        
        nGameList = [nGames//nProc]*nProc
        nGameList[-1] += (nGames % nProc)
        
        if verbose:
            print 'Running parallel simulation.'
            print 'Number of cores = {0}'.format(nProc)
            print 'Number of simulations per core = {0}'.format(nGameList)
            print 'Total Number of simulations = {0}'.format((sum(nGameList)))
            
        results = []
        
        for p in xrange(nProc):
            print 'p = {0}'.format(p)
            results.append(pool.apply_async(simulateAuction, kwds = {'agentType':agentType,
                                                                    'parallel':False,
                                                                    'pricePrediction':pricePrediction,
                                                                    'minPrice': minPrice,
                                                                    'maxPrice': maxPrice,
                                                                    'minValuation':minValuation,
                                                                    'maxValuation':maxValuation,
                                                                    'm':m,
                                                                    'nGames':nGameList[p],
                                                                    'verbose':verbose}))
            
        pool.close()
        pool.join()
            
        start_row = 0
        end_row = 0
        for idx, r in enumerate(results):
            end_row += nGameList[idx]*nAgents
            bids[start_row:end_row,:] = r.get()
            results[idx]._value = []
            start_row = end_row
        
    else:
        agents = [agentFactory(agentType = atype, m = m, vmin = minValuation, vmax = maxValuation) for atype in agentType]
        
        
        for itr in xrange(nGames):
            
            if verbose:
                print 'running serial game {0}'.format(itr)
            
            if isinstance(pricePrediction,list):
                
                for idx, agent, pp in zip(numpy.arange(nAgents),agents,pricePrediction):
                    agent.randomValuation()
                    bids[itr*nAgents + idx,:] = agent.bid(pricePrediction = pp)
                    
            else:
                for idx, agent in enumerate(agents):
                    agent.randomValuation()
                    if verbose:
                        print "agent[{0}].l        = {1}".format(idx,agent.l)
                        print "agent[{0}].v        = {1}".format(idx,agent.v)
                        
                    bids[itr*nAgents + idx,:] = agent.bid(pricePrediction = pricePrediction)
                    
                    if verbose:
                        print "agent[{0}].bid(...) = {1}".format(idx,bids[itr,:])
                    
    return bids
       