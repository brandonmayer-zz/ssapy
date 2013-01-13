from ..marketSchedule import listRevenue
from .msAgent import msAgent
from ...strategies.straightMU import straightMU as strategies

class straightMUa(msAgent):
    def __init__(self, **kwargs):
        super(straightMUa, self).__init__(**kwargs)
        
    def bid(self, **kwargs):
        pricePrediction = kwargs.get('pricePrediction')
        
        bundles = kwargs.get('bundles', self.listBundles())
        
        revenue = kwargs.get('revenue', listRevenue(bundles, self.v, self.l))
        
        verbose = kwargs.get('verbose',False)
        
        return strategies.straightMUa(bundles, revenue, pricePrediction, verbose)
                                     
class straightMU8(msAgent):
    def __init__(self, **kwargs):
        super(straightMU8, self).__init__(**kwargs)
        
    def bid(self, **kwargs):
        
        pricePrediction = kwargs.get('pricePrediction')
        
        bundles = kwargs.get('bundles', self.listBundles())
        
        revenue = kwargs.get('revenue', listRevenue(bundles, self.v, self.l))
        
        verbose = kwargs.get('verbose',False)
        
        return strategies.straightMU8(bundles, revenue, pricePrediction, verbose)
    
    
class straightMU64(msAgent):
    def __init__(self, **kwargs):
        super(straightMU64, self).__init__(**kwargs)
        
    def bid(self, **kwargs):
        pricePrediction = kwargs.get('pricePrediction')
        
        bundles = kwargs.get('bundles', self.listBundles())
        
        revenue = kwargs.get('revenue', listRevenue(bundles, self.v, self.l))
        
        verbose = kwargs.get('verbose',False)
        
        return strategies.straightMU64(bundles, revenue, pricePrediction, verbose)
    
class straightMU256(msAgent):
    def __init__(self,**kwargs):
        super(straightMU256, self).__init__(**kwargs)
        
    def bid(self, **kwargs):
        pricePrediction = kwargs.get('pricePrediction')
        
        bundles = kwargs.get('bundles', self.listBundles())
        
        revenue = kwargs.get('revenue', listRevenue(bundles, self.v, self.l))
        
        verbose = kwargs.get('verbose', False)
        
        return strategies.straightMU256(bundles, revenue, pricePrediction, verbose)
        
        
    