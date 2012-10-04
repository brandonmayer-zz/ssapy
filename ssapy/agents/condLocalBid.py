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
                
                newBid = 0.0
                
                for bundleIdx, bundle in enumerate(bundles[bundles[bidIdx] == 0]):
                    
                    
                    