import numpy
from ssapy.agents.marketSchedule import listRevenue
from ssapy.pricePrediction import jointGMM
from ssapy.strategies.jointLocal import jointLocal as jointLocalStrategy
from ssapy.util import listBundles
from ssapy.strategies.strategyFactory import strategyFactory

from .msAgent import msAgent

class jointLocal(msAgent):
    def __init__(self, **kwargs):
        super(jointLocal, self).__init__(**kwargs)
        
        self.initStrategy = kwargs.get('initStrategy', strategyFactory('straightMU8'))
        
        self.maxItr       = kwargs.get('maxItr',100)
        
        self.tol          = kwargs.get('tol',1e-5)
        
        self.verbose      = kwargs.get('verbose',False)
        
        self.ret          = kwargs.get('ret','bids')
        
        self.nsamples     = kwargs.get('nsamples', 10000)
        
    def bid(self,**kwargs):
        pricePrediction = kwargs.get('pricePrediction', self.pricePrediction)
        
        bundles         = kwargs.get('bundles', self.listBundles())
        
        revenue         = kwargs.get('revenue', listRevenue(bundles, self.v, self.l))
        
        verbose         = kwargs.get('verbose', False)
        
        initStrategy    = kwargs.get('initStrategy', self.initStrategy)
        
        maxItr          = kwargs.get('maxItr', self.maxItr)
        
        tol             = kwargs.get('tol', self.tol)
        
        verbose         = kwargs.get('verbose', self.verbose)
        
        ret             = kwargs.get('ret', self.ret)
        
        nsamples        = kwargs.get('nsamples', self.nsamples)
        
        initBids        = kwargs.get('initBids',initStrategy(bundles, revenue, pricePrediction))
        
        samples         = pricePrediction.sample(n_samples = nsamples)
        
        return jointLocalStrategy(bundles, revenue, initBids, samples, maxItr, tol, verbose, ret)          