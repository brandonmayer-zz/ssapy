"""
this is /auctionSimulator/hw4/agents/straightMU.py

Author: Brandon Mayer
Date:   11/21/2011

Specialized agent class to replicate straightMU from Yoon and Wellman 2011.
This is just a wrapper around targetMV and accepts a price prediction distribution
and calculates the mean(s) for price prediction
"""
from margDistPredictionAgent import *
from straightMV import *
import copy

class straightMU(margDistPredictionAgent):
    def __init__(self,**kwargs):
        super(straightMU,self).__init__(**kwargs)
        
#        self._bundles = kwargs.get('bundles',self.allBundles(self.m))
#        self._valuation= kwargs.get('valuation',self.valuation(self._bundles, self.v, self.l))
        
               
    @staticmethod
    def type():
        return "straightMU"
    
    @staticmethod
    def SS(**kwargs):
        """
        Calculate the expected marginal price vector given marginal distributions
        over good prices. 
        
        We consider in the average, the price associated with a bin to be the
        bins center. The average is then calculated as summing the product 
        of the bin centers multiplied by the bin probability.
        """
        expectedPrices = None
        if 'expectedPrices' in kwargs:
            expectedPrices = kwargs['expectedPrices']
        else:
            #check validity of args
            pricePrediction = margDistPredictionAgent.SS(**kwargs)
            
            #AGENT SPECIFIC LOGIC
            expectedPrices = kwargs.get('expectedPrices',pricePrediction.expectedPrices())            

        return straightMV.SS(pointPricePrediction = expectedPrices,
                             bundles              = kwargs['bundles'],
                             l                    = kwargs['l'],
                             valuation            = kwargs['valuation'])
        
    def bid2(self,**kwargs):
        
        expectedPrices = numpy.asarray(kwargs.get('expectedPrices'))
        m              = kwargs.get('m',self.m)
        bundles        = kwargs.get('bundles',self.allBundles(m))
        l              = kwargs.get('l',self.l)
        v              = kwargs.get('v',self.v)
        valuation      = kwargs.get('valuation',self.valuation(bundles, v, l))
        
        return straightMV.SS( pointPricePrediction = expectedPrices,
                              bundles              = bundles,
                              l                    = l,
                              valuation            = valuation)
               
class straightMU8(margDistPredictionAgent):
    """
    A concrete class for straightMU8
    """
    @staticmethod
    def type():
        return "straightMU8"
    
    @staticmethod
    def SS(**kwargs):
        """
        Calculate the expected using inverse sampling method and 8 samples
        Then bid via straightMV with the resulting expected prices
        """
        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        if 'expectedPrices' not in kwargs:
            expectedPrices = pricePrediction.expectedPrices( method   = 'iTsample',
                                                             nSamples = 8)
        
        bundles = kwargs.get('bundles', simYW.allBundles(pricePrediction.m))
        
        return straightMU.SS( expectedPrices = expectedPrices,
                              bundles        = bundles,
                              valuation      = kwargs['valuation'],
                              l              = kwargs['l'])
        
    def printSummary(self,**kwargs):
        tkwargs = copy.deepcopy(kwargs)
        if 'expectedPrices' not in kwargs:
            
            tkwargs['method']   = 'iTsample'
            tkwargs['nSamples'] = 8
            
        super(straightMU8,self).printSummary(**tkwargs)
        
class straightMU64(margDistPredictionAgent):
    """
    A concrete class for straightMU64
    """
    @staticmethod
    def type():
        return "straightMU64"
    
    @staticmethod
    def SS(**kwargs):
        """
        Calculate the expected using inverse sampling method and 8 samples
        Then bid via straightMV with the resulting expected prices
        """
        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        expectedPrices = pricePrediction.expectedPrices( method   = 'iTsample',
                                                         nSamples = 64)
        
        bundles = kwargs.get('bundles', simYW.allBundles(pricePrediction.m))
        
        return straightMU.SS( expectedPrices = expectedPrices,
                              bundles        = bundles,
                              valuation      = kwargs['valuation'],
                              l              = kwargs['l'])
                
        
    def printSummary(self,**kwargs):
        tkwargs = copy.deepcopy(kwargs)
        if 'expectedPrices' not in kwargs:
            
            tkwargs['method']   = 'iTsample'
            tkwargs['nSamples'] = 64
            
        super(straightMU64,self).printSummary(**tkwargs)
        
class straightMU256(margDistPredictionAgent):
    """
    A concrete class for straightMU64
    """
    @staticmethod
    def type():
        return "straightMU256"
    
    @staticmethod
    def SS(**kwargs):
        """
        Calculate the expected using inverse sampling method and 8 samples
        Then bid via straightMV with the resulting expected prices
        """
        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        expectedPrices = pricePrediction.expectedPrices( method   = 'iTsample',
                                                         nSamples = 256)
        
        bundles = kwargs.get('bundles', simYW.allBundles(pricePrediction.m))
        
        return straightMU.SS( expectedPrices = expectedPrices,
                              bundles        = bundles,
                              valuation      = kwargs['valuation'],
                              l              = kwargs['l'])
        
    def printSummary(self,**kwargs):
        tkwargs = copy.deepcopy(kwargs)
        if 'expectedPrices' not in kwargs:
            
            tkwargs['method']   = 'iTsample'
            tkwargs['nSamples'] = 256
            
        super(straightMU256,self).printSummary(**tkwargs)