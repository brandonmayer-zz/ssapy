import numpy

def expectedValution(pricePrediction, bundles, valuation, bids):
    expVal = 0.0
    for bundleIdx, bundle in enumerate(bundles):
        expVal += (valuation[bundleIdx]*pricePrediction.pWin(bundle,bids))
    return expVal

def expectedCost(pricePrediction, bundles, valuation, bids, qmin = 0.5, qstep = 1):
    expCost = 0.0
    for goodIdx in xrange(bundles.shape[1]):
        ep = 0.0
        for q in numpy.arange(qmin,bids[goodIdx],qstep):
            ep += (q*pricePrediction.eval(q,goodIdx))
        ep += bids[goodIdx]*pricePrediction.eval(bids[goodIdx],goodIdx)
        expCost += ep
        
    return expCost

def highestOtherBids(bids, targetIdx):
    otherAgents = numpy.delete(numpy.arange(bids.shape[1]),targetIdx)
    
    hob = numpy.max(bids[otherAgents],1)
    
    return hob

class uniformpp(object):
    """
    A uniform price prediction for scpp initialization
    """
    def __init__(self,m = 5, minPrice = 0, maxPrice = 50):
        self.m = m
        self.minPrice = minPrice
        self.maxPrice = maxPrice
        
    def sample(self,n_samples = 1):
        return numpy.random.rand(n_samples,self.m)*(self.maxPrice-self.minPrice)+self.minPrice
    
    def expectedValue(self):
        return numpy.ones(self.m)*(self.maxPrice-self.minPrice)*0.5