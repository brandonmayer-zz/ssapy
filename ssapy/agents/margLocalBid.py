from ssapy.agents.margDistPredictionAgent import margDistPredictionAgent
from ssapy.pricePrediction.jointGMM import jointGMM
from ssapy.pricePrediction.margDistSCPP import margDistSCPP
import ssapy.agents.agentFactory

from scipy.stats import norm
from scipy.interpolate import interp1d

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
            
        #precompute cdfs for speed
        cdf = []
        if isinstance(pricePrediction,margDistSCPP):
            for hist,binEdges in pricePrediction.data:
                p = hist / numpy.float(numpy.dot(hist, numpy.diff(binEdges)))
                c = numpy.cumsum(p*numpy.diff(binEdges),dtype=numpy.float)
                f = interp1d(binEdges[:-1],c,'linear')
                cdf.append(f)
                
        
        for itr in xrange(n_itr):
            if verbose:
                print "itr = {0}, bid = {1}".format(itr,bids)
                
            prevBid = bids.copy()
            
            for bidIdx in xrange(bids.shape[0]):
                
                newBid = 0.0
#                posTarget = bundles[bundles[:,bidIdx] == True]
#                negTarget = posTarget
#                negTarget[:,bidIdx] = False
                otherGoods = numpy.delete(numpy.arange(bids.shape[0]),bidIdx)
                
#                for posBundle,negBundle in zip(posTarget,negTarget):
                for posBundle in bundles[bundles[:,bidIdx] == True]:
                    negBundle = posBundle.copy()
                    negBundle[bidIdx] = False
                    
                    v1 = bundleValueDict[tuple(posBundle)]
                    v0 = bundleValueDict[tuple(negBundle)]
                    
                    if isinstance(pricePrediction, jointGMM):
                        p = 1.0
                        for og in otherGoods:
                            if posBundle[og] == True:
                                p *= pricePrediction.margCdf(x = bids[og], margIdx = og)
                            else:
                                p *= (1- pricePrediction.margCdf(x = bids[og], margIdx = og))
                                    
                    elif isinstance(pricePrediction, margDistSCPP):

                        p = 1.0
                        for og in otherGoods:
                            if bids[bidIdx] > pricePrediction.data[bidIdx][1][-1]:
                                pass
                            elif bids[bidIdx] < pricePrediction.data[bidIdx][1][-1]:
                                p *= 1e-5
                            elif posBundle[og] == True:
                                p*=cdf[og](bids[bidIdx])
                            else:
                                p*=1-cdf[og](bids[bidIdx])
                                    
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
                    
            if numpy.dot(prevBid - bids,prevBid - bids) <= tol:
                if verbose:
                    print ''
                    print 'localBid terminated.'
                    print 'prevBid = {0}'.format(prevBid)
                    print 'bids    = {0}'.format(bids)
                    print 'sse     = {0}'.format(numpy.dot(prevBid - bids,prevBid - bids))
                break
                
                
                
        return bids
                
            
                     
                
        
        
        
        
        