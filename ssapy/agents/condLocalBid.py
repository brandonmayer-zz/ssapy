"""
An agent to bid local conditional marginal revenue given a joint distribution
"""

from margDistPredictionAgent import margDistPredictionAgent
from agentFactory import agentFactory

import numpy

class condLocalBid(margDistPredictionAgent):
    @staticmethod
    def type():
        return "condLocalBid"
    
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
                print "itr = {0}, bids = {1}".format(itr,bids)
                
            for bidIdx, bid in enumerate(bids):
                
                goodsWon = samples <= bids
                
                targetWon  = samples[goodsWon[:,bidIdx]==True,:]
                normWon = targetWon.shape[0] + 1
                
                targetLost = samples[goodsWon[:,bidIdx] == False,:]
                normLost = targetLost.shape[0] + 1
                
                newBid = 0.0
                
                for bundleIdx, posBundle in enumerate(bundles[bundles[:,bidIdx]==True]):
                    negBundle = posBundle.copy()
                    negBundle[bidIdx] = False
                    
                    newBid += (numpy.float( bundleValueDict[tuple(posBundle)] * (numpy.count_nonzero( targetWon == posBundle ) + 1) )/ normWon) -\
                              (numpy.float( bundleValueDict[tuple(negBundle)] * (numpy.count_nonzero( targetLost == negBundle) + 1) )/ normLost) 
                              
                bids[bidIdx] = newBid
                
        return bids
                
                # number of goods that won with the b_j
                # to avoid divide by zero pad with 1 count in each half (win / lose b_j) 
                # then re-normalize by adding 2 to the number of samples.
                # equivalent to uniform dirichlet prior
#                norm1 = numpy.float( numpy.count_nonzero(goodsWon[bidIdx]) + 1 ) / (samples.shape[0] + 2)
#                
#                # number of goods that lost w.r.t to b_j
#                norm0 = numpy.float(1.0) - norm1
#                
#                for bundleIdx, bundle in enumerate(bundles[bundles[bidIdx] == 1]):
#                    
#                    bundleCopy = bundle.copy()
#                    bundleCopy = ~bundleCopy[bidIdx]
#                    
#                    v1 = bundleValueDict[tuple(bundle)]
#                    v0 = bundleValueDict[tuple(bundleCopy)]
#                    
#                    p1 = numpy.count_nonzero(numpy.all(goodsWon == bundle,1))/ numpy.float( numpy.count_nonzero(goodsWon[bidIdx]) + 1 )
                    
if __name__ == "__main__":
    from simYW import simYW
    from sklearn.datasets import make_blobs
    import sklearn
    from ssapy.pricePrediction.jointGMM import jointGMM
    
    m=2
    
    v, l = simYW.randomValueVector(0, 50, m, l = 1)
    
    print "v = {0}".format(v)
    print "l = {0}".format(l)
    
    bundles = simYW.allBundles(nGoods=m)
    
    valuation = simYW.valuation(bundles, v, l)
    
    pricePrediction = jointGMM(n_components=3)
    
    x,y = make_blobs(n_samples=1000,centers = [[5,5],[15,20],[20,30]], n_features = 2)
    
    pricePrediction.fit(x)
    
    bids = condLocalBid.SS(bundles = bundles,
                       valuation = valuation,
                       pricePrediction=pricePrediction,
                       l = l,
                       verbose = True,
                       nSamples = 10)
    
    print bids                 
                    
                    
                    
                    