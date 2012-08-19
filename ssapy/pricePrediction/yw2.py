import numpy

from ssapy.multiprocessingAdaptor import Consumer
from ssapy.agents.agentFactory import agentFactory
from ssapy.pricePrediction.margDistSCPP import margDistSCPP

from ssapy.pricePrediction.util import klDiv, ksStat, updateDist

import json
import multiprocessing
import os
import time

def simulateAuction( **kwargs ):
    agentType     = kwargs.get('agentType')
    nAgents       = kwargs.get('nAgents')
    margDist      = kwargs.get('margDist')
    nGames        = kwargs.get('nGames')
    m             = margDist.m

    winningBids = numpy.zeros((nGames,m))
    
    for g in xrange(nGames):
        agentList = [agentFactory(agentType = agentType, m = m) for i in xrange(nAgents)]
    
        bids = numpy.atleast_2d([agent.bid(margDistPrediction = margDist) for agent in agentList])
        
        winningBids[g,:] = numpy.max(bids,0)
#    return numpy.max(bids,0)
    return winningBids

class yw2Task(object):
    def __init__(self, **kwargs):
        self.agentType = kwargs.get('agentType')
        self.nAgents   = kwargs.get('nAgents')
        self.margDist  = kwargs.get('margDist')
        self.nGames    = kwargs.get('nGames')
        
    def __call__(self):
        
#        winningBids = numpy.zeros((self.nGames,self.margDist.m))
#        for i in xrange(self.nGames):
#            winningBids[i,:] = simulateAuction(agentType = self.agentType, 
#                                               nAgents = self.nAgents, 
#                                               margDist = self.margDist)
#            
#        return winningBids
        return simulateAuction(agentType = self.agentType,
                               nAgents   = self.nAgents,
                               margDist  = self.margDist,
                               nGames    = self.nGames)
    
    
def yw2SCPP(**kwargs):
    oDir = kwargs.get('oDir')
    if not oDir:
        raise ValueError("Must provide oDir")
    oDir = os.path.realpath(oDir)
    
    agentType = kwargs.get('agentType')
    nAgents   = kwargs.get('nAgents',8)
    m         = kwargs.get('m', 5)
    L         = kwargs.get('L',100)
    d         = kwargs.get('d', 0.01)
    g         = kwargs.get('g', 1000000)
    minPrice  = kwargs.get('minPrice',0)
    maxPrice  = kwargs.get('maxPrice',50)
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
    
    
    if not serial:
        nGamesList = [g/nProc]*nProc
        nGamesList[-1] += (g%nProc)
    
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
    for t in xrange(0,L):
        
        if pltItr:
            cs = cs = ['y--p', 'm-*', 'r-o','y-^','y-*']
            graphname = os.path.join(oDir,'ywSCPP_itr_{0}.png'.format(t))
            if not ksList:
                title = "yw2SCPP, {0}, \n itr = {1}".format(agentType,t)
            else:
                title = "ywSCPP, {0} \n kld = {1}, ks = {2} \nitr = {3}".format(agentType,klList[-1],ksList[-1],t)
            currentDist.graphPdfToFile(fname = graphname,
                                       colorStyles = cs,
                                       title = title)
        
        if verbose:
            print ""
            print 'Iteration = {0}'.format(t)
            
        if dampen:
            kappa = float(L - t) / L
        else:
            kappa = 1
            
        if serial:
            result = numpy.zeros(g,m)
            for i in xrange(g):
                result[i,:] = simulateAuction(agentType = agentType, nAgents = nAgents, margDist = currentDist) 
                
        else:
            tasks = multiprocessing.JoinableQueue()
            
            results = multiprocessing.Queue()
            
            consumers = [Consumer(tasks,results) for i in xrange(nProc)]
            
            #start the consumers
            [w.start() for w in consumers]
                     
            [tasks.put( yw2Task(agentType = agentType, nAgents = nAgents, margDist = currentDist, nGames = nGames) ) for nGames in nGamesList]
            
            [tasks.put(None) for i in xrange(nProc)]
            
            if verbose:
                start = time.time()
                print "Waiting for {0} game simulation Simulation...".format(g)
                
            tasks.join()
            
            if verbose:
                print ""
                print "Finished {0} simulations in {1} seconds.".format(g,time.time()-start)
            
            if verbose:
                print ""
                print "Collecting Results"
                start = time.time()
             
            
            
               
            rList = []
            while not results.empty():
                rList.append(results.get())
                
            result = numpy.vstack(rList)
            
            if verbose:
                print ""
                print "Done collecting results in {0} seconds".format(time.time() - start)
                
            [w.terminate() for w in consumers]
            del results,tasks,consumers
        
            
        histData = [] 
        histCount = []
        for m in xrange(result.shape[1]):
            histData.append(numpy.histogram(result[:,m],binEdges,density=True))
#            histCount.append(numpy.histogram(result[:,m],binEdges,density=False))
            
        newDist = margDistSCPP(histData)  
        ksList.append(ksStat(currentDist, newDist))
        klList.append(klDiv(currentDist, newDist))
        
        if ksList[-1] < d or t == (L-1):
            
            postfix = '{0}_{1}_{2}_{3}_{4}_{5}'.format(agentType, g, m, d,minPrice,maxPrice)
            pklName = 'distPricePrediction_' + postfix + '.pkl'
            txtName = 'distPricePrediction_' + postfix + '.txt'
            
            pricePredictionPklFilename = os.path.join(oDir, pklName) 
                                                      
            currentDist.savePickle(pricePredictionPklFilename)
            
            pricePredictionTxtFilename = os.path.join(oDir, txtName)
            
            #this section could be improved....
            testdata = []
            for m in xrange(currentDist.m):
                if m == 0:
                    textdata = numpy.vstack([currentDist.data[m][0],currentDist.data[m][1][:-1]])
                else:
                    textdata = numpy.vstack([textdata, numpy.vstack([currentDist.data[m][0],currentDist.data[m][1][:-1]])])
                    
            numpy.savetxt(pricePredictionTxtFilename,textdata)
            
            print ''
            print'Terminated after {0} Iterations'.format(t)
            print'Final Expected Price Vector = {0}'.format(currentDist.expectedPrices())
            
            ksListName = os.path.join(oDir,'ksList.json')
            with open(ksListName,'w') as f:
                json.dump(ksList,f)
            klListName = os.path.join(oDir,'klList.json')
            with open(klListName,'w') as f:
                json.dump(klList,f)
            
            break
        else:
            
            currentDist = updateDist(currentDist, newDist, kappa)
            del result, newDist
            
        
        
if __name__ == "__main__":
    oDir = "C:/auctionResearch/experiments/yw2/debug"
    agentType = "targetMU8"
    minPrice  = 0
    maxPrice  = 50
    m         = 5
    L         = 100
    d         = 0.01
    g         = 5
    tempDist = []
    p = float(1)/round(maxPrice - minPrice)
    a = [p]*(maxPrice - minPrice)
#    binEdges = [bin for bin in xrange( int(minPrice - maxPrice)+1 ) ]
    binEdges = numpy.arange(minPrice,maxPrice+1,1)
    for i in xrange(m):
        tempDist.append((numpy.atleast_1d(a),numpy.atleast_1d(binEdges)))
    
    margDist = margDistSCPP(tempDist)
    
    task = yw2Task(agentType = "straightMU8", nAgents = 8, margDist = margDist, nGames = 1)
        
    winningBids = task()

#    yw2SCPP(oDir = oDir, agentType = agentType, minPrice = minPrice, maxPrice = maxPrice, m = m, L = L, d = d, g = g)
    
    pass    
             
        
