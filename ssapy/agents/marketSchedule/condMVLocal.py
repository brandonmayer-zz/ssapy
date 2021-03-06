from ..marketSchedule import listRevenue
from .msAgent import msAgent
from ...strategies import straightMU as strategies
from ...strategies.condLocal import condMVLocal as cmv

from ...strategies.strategyFactory import strategyFactory

class condMVLocal(msAgent):
    def __init__(self,**kwargs):
        super(condMVLocal, self).__init__(**kwargs)
        
    def bid(self, **kwargs):
        pricePrediction = kwargs.get('pricePrediction', self.pricePrediction)
        
        bundles = kwargs.get('bundles',self.listBundles())
        
        revenue = kwargs.get('revenue',self.listRevenue())
        
        initss = kwargs.get('initss','straightMU8')
        
        verbose = kwargs.get('verbose', False)
        
        nsamples = kwargs.get('nsamples',1000)
        
        samples = kwargs.get('samples',pricePrediction.sample(n_samples = nsamples))
        
        maxItr = kwargs.get('maxItr',100)
        
        initBids = kwargs.get('initBids')
        
        if initBids == None:
            initialStrategy = strategyFactory(initss)
            
            initbids = initialStrategy(bundles, revenue, pricePrediction, verbose)
            
        tol = kwargs.get('tol',1e-5)
        
        ret = kwargs.get('ret','bids')
            
        bids = cmv(bundles, revenue, initbids, samples, maxItr, tol, verbose, ret)
        
        return bids 