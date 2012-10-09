from ssapy.agents.margDistPredictionAgent import margDistPredictionAgent
from ssapy.pricePrediction.jointGMM import jointGMM
import ssapy.agents.agentFactory

import numpy
import matplotlib.pyplot as plt

class margLocalBid(margDistPredictionAgent):
    def __init__(self,**kwargs):
        #put import in init to avoid circlular imports when
        #agentFactory imports localbid
        from ssapy.agents.agentFactory import agentFactory
        
        super(margLocalBid, self).__init__(**kwargs)
        
    @staticmethod
    def type():
        return "localBid"
        
    @staticmethod
    def SS(**kwargs):
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("localBid.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("localBid.SS(...) - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("localBid.SS(...) - must specify l (target number of time slots)")
        
        viz = kwargs.get('viz',False)
        if viz:
            bidList = []
        
        n_itr = kwargs.get('n_itr', 100)
        
        tol = kwargs.get('tol',1e-8)
        
        initialBidderType = kwargs.get('initialBidder','straightMU8')
        
        verbose = kwargs.get('verbose',False)
        
        pricePrediction = kwargs.get('pricePrediction')
        
        if pricePrediction == None:
            raise KeyError("localBid.SS(...) - must specify pricePrediction")
        
        initialBidder = ssapy.agents.agentFactory.agentFactory(agentType = initialBidderType,
                                                               m = bundles.shape[1])
        
        bids = initialBidder.SS(pricePrediction = pricePrediction,
                                bundles = bundles,
                                valuation = valuation,
                                l = l)
        
        del initialBidder
        
        bundleValueDict = dict([(tuple(b),v) for b, v in zip(bundles,valuation)])
        
        del valuation
        
        if viz:
            bidList.append(bids)
        
        for itr in xrange(n_itr):
            if verbose:
                print "itr = {0}, bid = {1}".format(itr,bids)
                
            prevBid = bids.copy()
            
            for bidIdx in xrange(bids.shape[0]):
                
                newBid = 0.0
                
                for posBundle in bundles[bundles[:,bidIdx] == True]:
                    negBundle = posBundle.copy()
                    negBundle[bidIdx] = False
                    
                    v1 = bundleValueDict[tuple(posBundle)]
                    v0 = bundleValueDict[tuple(negBundle)]
                    
                    otherGoods = numpy.delete(numpy.arange(bids.shape[0]),bidIdx)
                    
                    p = 1.0
                    for og in otherGoods:
                        
                        if isinstance(pricePrediction, jointGMM):
                            if posBundle[og] == True:
                                p *= pricePrediction.margCdf(x = bids[og], margIdx = og)
                            else:
                                p *= (1- pricePrediction.margCdf(x = bids[og], margIdx = og))
                                
                    newBid += (v1 - v0)*p
                    
                bids[bidIdx] = newBid
                
                if verbose:
                    print ''
                    print 'Iteration = {0}'.format(itr)
                    print 'prevBid   = {0}'.format(prevBid)
                    print 'newBid    = {0}'.format(bids)
                
                if viz:
                    bidList.append(bids)
                    plt.plot(bidList[:-1],'bo',markerfacecolor=None)
                    plt.plot(bidList[-1],'ro')
                    plt.show()
                    
                if numpy.dot(prevBid - bids,prevBid - bids) <= 1e-8:
                    if verbose:
                        print ''
                        print 'localBid terminated.'
                        print 'prevBid = {0}'.format(prevBid)
                        print 'bids    = {0}'.format(bids)
                        print 'sse     = {0}'.format(numpy.dot(prevBid - bids,prevBid - bids))
                    break
                
                
                
            return bids
                
            
                     
                
        
        
        
        
        