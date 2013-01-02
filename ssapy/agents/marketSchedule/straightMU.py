from ssapy.agents.marketSchedule import msAgent, listRevenue
import ssapy.strategies.straightMU as strategies
from ssapy.util import listBundles

class straightMU8(msAgent):
    def __init__(self, **kwargs):
        super(straightMU8, self).__init__(**kwargs)
        
    def bid(self, **kwargs):
        
        pricePrediction = kwargs.get('pricePrediction')
        
        bundles = kwargs.get('bundles', listBundles(self.m))
        
        revenue = kwargs.get('revenue', listRevenue(bundles, self.v, self.l))
        
        verbose = kwargs.get('verbose',False)
        
        return strategies.straightMU8(bundles, revenue, pricePrediction, verbose)
    
    
class straightMU64(msAgent):
    def __init__(self, **kwargs):
        super(straightMU64, self).__init__(**kwargs)
        
    def bid(self, **kwargs):
        pricePrediction = kwargs.get('pricePrediction')
        
        bundles = kwargs.get('bundles', listBundles(self.m))
        
        revenue = kwargs.get('revenue', listRevenue(bundles, self.v, self.l))
        
        verbose = kwargs.get('verbose',False)
        
        return strategies.straightMU64(bundles, revenue, pricePrediction, verbose)
    
class straightMU256(msAgent):
    def __init__(self,**kwargs):
        super(straightMU256, self).__init__(**kwargs)
        
    def bid(self, **kwargs):
        pricePrediction = kwargs.get('pricePrediction')
        
        bundles = kwargs.get('bundles', listBundles(self.m))
        
        revenue = kwargs.get('revenue', listRevenue(bundles, self.v, self.l))
        
        verbose = kwargs.get('verbose', False)
        
        return strategies.straightMU256(bundles, revenue, pricePrediction, verbose)
        
        
    