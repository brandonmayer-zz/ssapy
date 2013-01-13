import ssapy.strategies.straightMV as straightMV_
from ssapy.util import listBundles
from ssapy.agents.marketSchedule import listRevenue

#from ssapy.agents.marketSchedule.msAgent import msAgent
from .msAgent import msAgent

class straightMV(msAgent):
    def __init__(self, **kwargs):
        super(straightMV, self).__init__(**kwargs)
        
    def bid(self, **kwargs):
        pricePrediction = kwargs.get('pricePrediction',self.pricePrediction)
        
        bundles = kwargs.get('bundles', self.listBundles())
        
        revenue = kwargs.get('revenue',
                               listRevenue(bundles, self.v, self.l))
                              
        return straightMV_(bundles = bundles, 
                        revenue = revenue, 
                        pricePrediction = pricePrediction)