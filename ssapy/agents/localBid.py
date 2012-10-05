"""
An agent to bid local marginal revenue given a joint distribution
"""

from margDistPredictionAgent import margDistPredictionAgent
from agentFactory import agentFactory

#from straightMU import straightMU8,straightMU64, straightMU256
#from targetMU import targetMU8, targetMU64, targetMU256
#from targetMUS import targetMUS8, targetMUS64, targetMUS256
#from averageMU import averageMU8, averageMU64, averageMU256

import numpy

class localBid(margDistPredictionAgent):
    @staticmethod
    def type():
        return "localBid"
    
    @staticmethod
    def SS(**kwargs):
        
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("targetMU.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("targetMU - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("targetMU - must specify l (target number of time slots)")
        
        samples = kwargs.get('samples')
        
        if samples is None:
            
            pricePrediction = kwargs.get('pricePrediction')
        
            if pricePrediction == None:
                raise KeyError("targetMU.SS(...) - must specify pricePrediction")
        
            nSamples = kwargs.get('nSamples', 10000)
            
            n_itr    = kwargs.get('n_itr', 100)
            
            initialBidderType = kwargs.get('initialBidder','straightMU8')
            
            initialBidder = agentFactory(agentType = initialBidderType,m = bundles.shape[1])
            
            bids = initialBidder.SS(pricePrediction = pricePrediction,
                                    bundles = bundles,
                                    valuation = valuation,
                                    l = l)
            
            del initialBidder
            
            samples = pricePrediction.sample(n_samples = nSamples)
            
        verbose = kwargs.get('verbose',False)
    
        bundleValueDict = dict([(tuple(b),v) for b, v in zip(bundles,valuation)])
        
        del valuation
        
        
        for itr in xrange(n_itr):
            if verbose:
                print "itr = {0}, bid = {1}".format(itr,bids)
            for bidIdx, bid in enumerate(bids):
                
                
                goodsWon = samples <= bids
                
                newBid = 0.0
                for bundleIdx, bundle in enumerate(bundles[bundles[:,bidIdx] == True]):
                    
                    bundleCopy = bundle.copy()
                    bundleCopy[bidIdx] = False
                    
                    v1 = bundleValueDict[tuple(bundle)]
                    v0 = bundleValueDict[tuple(bundleCopy)]
                    
                    p = numpy.float(numpy.count_nonzero(numpy.all(goodsWon == bundle,1)) + \
                                    numpy.count_nonzero(numpy.all(goodsWon==bundleCopy,1))) / (nSamples)
                                        
                    bids[bidIdx] = (v1 - v0)*p
                
        return bids
        
if __name__ == "__main__":
    from simYW import simYW
    from sklearn.datasets import make_blobs
    import sklearn
    from ssapy.pricePrediction.jointGMM import jointGMM
    m=2
    
    
    
    v, l = simYW.randomValueVector(0, 50, m)
    
    print "v = {0}".format(v)
    print "l = {0}".format(l)
    
    bundles = simYW.allBundles(nGoods=m)
    
    valuation = simYW.valuation(bundles, v, l)
    
    pricePrediction = jointGMM(n_components=3)
    
    x,y = make_blobs(n_samples=1000,centers = [[5,5],[15,20],[20,30]], n_features = 2)
    
    pricePrediction.fit(x)
    
    bids = localBid.SS(bundles = bundles,
                       valuation = valuation,
                       pricePrediction=pricePrediction,
                       l = l,
                       verbose = True,
                       nSamples = 10000)
    
    print bids
    
    
    
    
    
    
    
                    
                    
        
        
        