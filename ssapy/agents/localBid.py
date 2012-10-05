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
import matplotlib.pyplot as plt

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
        
        plot2d = kwargs.get('plot2d',False)

        
        if samples is None:
            
            pricePrediction = kwargs.get('pricePrediction')
        
            if pricePrediction == None:
                raise KeyError("targetMU.SS(...) - must specify pricePrediction")
        
            nSamples = kwargs.get('nSamples', 10000)
            
            samples = pricePrediction.sample(n_samples = nSamples)
                       
        n_itr = kwargs.get('n_itr', 100)
            
        initialBidderType = kwargs.get('initialBidder','straightMU8')
            
        initialBidder = agentFactory(agentType = initialBidderType,m = bundles.shape[1])
            
        bids = initialBidder.SS(pricePrediction = pricePrediction,
                                bundles = bundles,
                                valuation = valuation,
                                l = l)
            
        del initialBidder
            
          
        verbose = kwargs.get('verbose',False)
    
        bundleValueDict = dict([(tuple(b),v) for b, v in zip(bundles,valuation)])
        
        del valuation
        
        
        for itr in xrange(n_itr):
            
            if verbose:
                print "itr = {0}, bid = {1}".format(itr,bids)
                
            if plot2d:
                plt.figure()
                plt.plot(samples[:,0],samples[:,1],'go', markersize =  10)
                plt.plot(bids[0],bids[1],'ro', markersize = 10)
                plt.axvline(x = bids[0], ymin=0, ymax = bids[1], color = 'b')
                plt.axvline(x = bids[0], ymin = bids[1], color = 'r')
                plt.axhline(y = bids[1], xmin = 0, xmax = bids[0], color = 'b')
                plt.axhline(y = bids[1], xmin = bids[0], color = 'r')
                
                plt.show()
                
            for bidIdx in xrange(bids.shape[0]):
                
                goodsWon = samples <= bids
            
                newBid = 0.0
                for bundle in bundles[bundles[:,bidIdx] == True]:
                    
                    bundleCopy = bundle.copy()
                    bundleCopy[bidIdx] = False
                    
                    v1 = bundleValueDict[tuple(bundle)]
                    v0 = bundleValueDict[tuple(bundleCopy)]

                    p = numpy.float( numpy.count_nonzero( numpy.delete(goodsWon,bidIdx,1) == numpy.delete(bundle,bidIdx) ) ) / nSamples                    

#                    bids[bidIdx] = (v1 - v0)*p
                    newBid += (v1 - v0)*p
                    
                    if verbose:
                        print ''
                        print "bid index = {0}".format(bidIdx)
                        print "bundle    = {0}".format(bundle)
                        print "v1        = {0}".format(v1)
                        print "v0        = {0}".format(v0)
                        print "p         = {0}".format(p)    
                        print "new Bid   = {0}".format(newBid)
                    
                bids[bidIdx] = newBid
                      
        return bids
    

        
if __name__ == "__main__":
    from simYW import simYW
    from sklearn.datasets import make_blobs
    import sklearn
    from ssapy.pricePrediction.jointGMM import jointGMM
    m=2
    
#    p1 = numpy.random.random(50)
#    p1 /= sum(p1)
#    
#    p2 = numpy.random.random(50)
#    p2 /= sum(p2)
    
    v, l = simYW.randomValueVector(0, 50, m)
    
    print "v = {0}".format(v)
    print "l = {0}".format(l)
    
    bundles = simYW.allBundles(nGoods=m)
    
    valuation = simYW.valuation(bundles, v, l)
    
    pricePrediction = jointGMM(n_components=3)
    
    x,y = make_blobs(n_samples=1000,centers = [[5,5],[15,20],[20,30]], n_features = 2)

#    x,y = make_blobs(n_samples=1000, centers = [5,5], n_features = 2)
    
    pricePrediction.fit(x)
    
    bids = localBid.SS(bundles = bundles,
                       valuation = valuation,
                       pricePrediction=pricePrediction,
                       l = l,
                       verbose = True,
                       nSamples = 1000,
                       plot2d = True)
    
    print bids
    
    
    
    
    
    
    
                    
                    
        
        
        