from . import msAgent, listRevenue
from ...strategies import targetPrice
from ...util import listBundles

class targetPrice8(msAgent):
    def __init__(self, **kwargs):
        super(targetPrice8, self).__init__(**kwargs)
    
    def bid(self, **kwargs):
        pricePrediction = kwargs.get('pricePrediction')
        bundles = kwargs.get('bundles',listBundles(self.m))
        revenue = kwargs.get('revenue',listRevenue(bundles, self.v, self.l))
        verbose = kwargs.get('verbose',False)
        
        return targetPrice.targetPrice8(bundles, revenue, pricePrediction, verbose)
    
class targetPrice64(msAgent):
    def __init__(self, **kwargs):
        super(targetPrice64, self).__init__(**kwargs)
    
    def bid(self, **kwargs):
        pricePrediction = kwargs.get('pricePrediction')
        bundles = kwargs.get('bundles',listBundles(self.m))
        revenue = kwargs.get('revenue',listRevenue(bundles, self.v, self.l))
        verbose = kwargs.get('verbose',False)
        
        return targetPrice.targetPrice64(bundles, revenue, pricePrediction, verbose)
    
class targetPrice256(msAgent):
    def __init__(self, **kwargs):
        super(targetPrice256, self).__init__(**kwargs)
    
    def bid(self, **kwargs):
        pricePrediction = kwargs.get('pricePrediction')
        bundles = kwargs.get('bundles',listBundles(self.m))
        revenue = kwargs.get('revenue',listRevenue(bundles, self.v, self.l))
        verbose = kwargs.get('verbose',False)
        
        return targetPrice.targetPrice256(bundles, revenue, pricePrediction, verbose)