import ssapy.strategies.straightMV as strategy
from ssapy.util import listBundles
from ssapy.agents.marketSchedule import msAgent, listRevenue

class straightMV(msAgent):
    def __init__(self, **kwargs):
        super(straightMV, self).__init__(**kwargs)
        
    def bid(self, **kwargs):
        pricePrediction = kwargs.get('pricePrediction',self.pricePrediction)
        
        bundles = kwargs.get('bundles', listBundles(self.m))
        
        valuation = kwargs.get('valuation',
                               listRevenue(bundles, self.v, self.l))
                              
        return strategy(bundles = bundles, 
                        valuation = valuation, 
                        pricePrediction = pricePrediction)
        
if __name__ == "__main__":
    import numpy
    pp = numpy.asarray([5,5])
    m = 2
    l = 1
    v = [20,10]
    
    agent = straightMV(m = m, l = l, v = v, pricePrediction = pp)
    #answer should be [15., 0.]
    print agent.bid()
    
    agent2 = straightMV(m=2)
    print 'v = {0}'.format(agent2.v)
    print 'l = {0}'.format(agent2.l)
    
    print 'agent2.bid = {0}'.format(agent2.bid(pricePrediction = pp))
    
    agent3 = straightMV(m=2)
    print 'v = {0}'.format(agent3.v)
    print 'l = {0}'.format(agent3.l)
    print 'agent3.bid = {0}'.format(agent3.bid(pricePrediction = pp))