"""
An agent to bid local conditional marginal revenue given a joint distribution
"""

from margDistPredictionAgent import margDistPredictionAgent
from agentFactory import agentFactory
import matplotlib.pyplot as plt

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
        
        viz = kwargs.get('viz',False)
        if viz and samples.shape[1] == 3:
            from mpl_toolkits.mplot3d import axes3d
            
        m = bundles.shape[1]
        
        for itr in xrange(n_itr):
            
            if verbose:
                print "itr = {0}, bids = {1}".format(itr,bids)
                
            if viz:
                if samples.shape[1] == 2:
                    plt.figure()
                    plt.plot(samples[:,0],samples[:,1],'go', markersize =  10)
                    plt.plot(bids[0],bids[1],'ro', markersize = 10)
                    plt.axvline(x = bids[0], ymin=0, ymax = bids[1], color = 'b')
                    plt.axvline(x = bids[0], ymin = bids[1], color = 'r')
                    plt.axhline(y = bids[1], xmin = 0, xmax = bids[0], color = 'b')
                    plt.axhline(y = bids[1], xmin = bids[0], color = 'r')
                    
                    plt.show()
                elif samples.shape[1] == 3:
                    fig = plt.figure()
                    ax = fig.gca(projection='3d')
                    ax.plot(samples[:,0],samples[:,1],samples[:,2],'go')
                    ax.plot([bids[0]], [bids[1]], [bids[2]],'bo')
                    
                    
                    plt.show()
                
            for bidIdx, bid in enumerate(bids):
                
                goodsWon = samples <= bids
                
                normWon = numpy.count_nonzero(goodsWon[:,bidIdx] == True)
                normLost = numpy.count_nonzero(goodsWon[:,bidIdx] == False)
                
                newBid = 0.0
                
                for bundleIdx, posBundle in enumerate(bundles[bundles[:,bidIdx]==True]):
                    negBundle = posBundle.copy()
                    negBundle[bidIdx] = False
                    
                    p1 = numpy.count_nonzero( numpy.all(goodsWon == posBundle, 1) ) + (numpy.float(1)/2**(m-1))
                    p1 = numpy.float(p1) / (normWon + 1)
                    
                    if p1 > 1.0:
                        raise ValueError ("p1 = {0} > 1.0".format(p1))
                    
                    if p1 < 0.0:
                        raise ValueError("p1 = {0} < 0.0".format(p1))
                    
                    p0 = numpy.count_nonzero( numpy.all(goodsWon == negBundle, 1) ) + (numpy.float(1)/2**(m-1))
                    p0 = numpy.float(p0) / ( normLost +  1 )
                    
                    if p0 > 1.0:
                        raise ValueError ("p0 = {0} > 1.0".format(p1))
                    
                    if p0 < 0.0:
                        raise ValueError("p0 = {0} < 0.0".format(p1))
                    
                    newBid += (bundleValueDict[tuple(posBundle)] * p1) - (bundleValueDict[tuple(negBundle)] * p0) 
                    
                    
                     
                              
                    if verbose:
                        print ''
                        print "bid index = {0}".format(bidIdx)
                        print "bundle    = {0}".format(posBundle)
                        print "v1        = {0}".format(bundleValueDict[tuple(posBundle)])
                        print "v0        = {0}".format(bundleValueDict[tuple(negBundle)])
                        print "p1        = {0}".format( p0 )
                        print "p0        = {0}".format( p1 )    
                        print "new Bid   = {0}".format(newBid)
                              
                if newBid >= 0.0:
                    bids[bidIdx] = newBid
                else:
                    bids[bidIdx] = 0.0
                
        return bids
                                    
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
                       nSamples = 10000,
                       viz = True)
                       
    
    print bids                 
                    
                    
                    
                    