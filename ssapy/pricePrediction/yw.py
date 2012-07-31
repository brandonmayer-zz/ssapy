from ssapy.multiprocessingAdaptor import Consumer
from ssapy.parallelWorker import parallelWorkerBase
from ssapy.auctions.simultaneousAuction import simultaneousAuction
from ssapy.pricePrediction.util import klDiv

from sklearn import mixture
import numpy

import multiprocessing
import time

class ywDPgmmTaskStraightMU8(parallelWorkerBase):
    def __init__(self,**kwargs):
        self.nAgents             = kwargs.get('nAgents',8)
        self.nGames              = kwargs.get('nGames')
        self.nSamples            = kwargs.get('nSamples',8)
        self.model               = kwargs.get('model')

    def __call__(self):
        
        if isinstance(self.model, mixture.GMM):
            for agentIdx in xrange(self.nAgents):
                samples = mixture.sample(8)
                logProb = mixture.eval(samples)
                prob    = numpy.exp(logProb)
                expectedPrice = numpy.dot(prob,samples)
                
    #            expectedPrices = 
        
        agentSurplus = []
        closingPrices = []
        for g in self.nGames:
            
            #draw a new valuation
            #maintain the same price prediction
            for agent in agentList:
                agent.randomValuation( vmin = self.pMin,
                                       vmax = self.pMax,
                                       m    = self.m)
                
                
                
            bids = [numpy.array(agent.bid()).astype('float') for agent in agentList]
        
            closingPrices.append(bids.max(0))
            
        return numpy.atleast_2d(closingPrices)
        
        


def ywDPgmm(**kwargs):
    #number of goods for auction
    m             = kwargs.get('m', 5)
    #list of participating agents
    agentTypeList = kwargs.get('agentTypeList',['straightMU8']*8)
    #number of inner loop games
    nTotGames     = kwargs.get('nGames', 1000000)
    #minimum price
    pmin          = kwargs.get('vmin',0)
    #maximum price
    pmax          = kwargs.get('vmax',50)
    #convergence histogram distance threshold
    d             = kwargs.get('d',0.01)
    #number of agents
    nAgents       = kwargs.get('nAgents', 8)
    #number of processors
    nProc         = kwargs.get('nProc', multiprocessing.cpu_count() - 1)
    
    #maximum number of iterations
    L             = kwargs.get('L')
    g             = kwargs.get('g')
    A             = kwargs.get('A')
    dampen        = kwargs.get('dampen',True)
    verbose       = kwargs.get('verbose',True)
    
    ksStat = numpy.zeros(L,dtype=numpy.float64)
    
    if verbose:
        print 'Computing Marginal DPVGMM Self Confirming Price Prediction'
        print 'agentTypeList = {0}'.format(agentTypeList)
        print 'd             = {0}'.format(d)
        print 'pMin          = {0}'.format(pMin)
        print 'pMax          = {0}'.format(pMax)
        print 'm             = {0}'.format(m)
        print 'nAgents       = {0}'.format(len(agentTypeList))
        print 'L             = {0}'.format(L)
        print 'dampen        = {0}'.format(dampen)
        print 'nProc         = {0}'.format(nProc)
    
    nGameList = []
    if nTotGames % (nProc-1) > 0:
        nGameList = [nTotGames/(nProc-1)]*(nProc-1)
        nGameList.append(nTotGames%(nProc-1))
    else:
        nGameList = [nTotGames/(nProc)]*nProc
        
    #create the initial uniform distribution
    tempDist = []
    p        = float(1)/round(pMax - pMin)
    a        = [p]*(pMax-pMin)
    binEdges = [bin for bin in xrange( int(args['maxPrice']-args['minPrice'])+1 ) ]
    for i in xrange(args['m']):
        tempDist.append((numpy.atleast_1d(a),numpy.atleast_1d(binEdges)))
        
    currentDist = margDistSCPP(tempDist)
        
    #clean up
    # keep the binEdges for later histograms
    del p,a,tempDist
    
    [consumers]
    
    kappa = 1
    for t in xrange(0,L):
        
        tasks = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()
        
        consumers = [Consumer(tasks, results) for i in xrange(nProc)]
        
        [w.start() for w in consumers]
        
        print ""
        
        if verbose:
            print "Iteration: {0}".format(t)
            
        if dampen:
            kappa = float(L-t)/L
            
        if verbose:
            print 'kappa = {0}'.format(kappa)
            gamesStart = time.time()
            
        for ng in nGameList:
            tasks.put(ywDPgmmTask(agentTypeList = agentTypeList,
                                  A             = A,
                                  nGames        = ng,
                                  margDistPrediction = currentDist))
          
        
        for ng in nGameList:
            tasks.put(None)
            
            
        closingPrices = []
        while not results.empty():
            closingPrices.append(numpy.atleast_2d(results.get()))
    
        closingPrices = numpy.atleast_2d(closingPrices)
    
def main():
    print 'hello yw'

if __name__ == "__main__":
    main()
    
