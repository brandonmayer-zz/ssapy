"""
this is /auctionSimulator/hw4/targetMU.py

Author: Brandon Mayer
Date:   11/21/2011

Specialized agent class to replicate targetMU from Yoon and Wellman 2011.
This is just a wrapper around targetMV and accepts a price prediction distribution
and calculates the mean(s) for price prediction
"""
from margDistPredictionAgent import *
from targetMV import *

from ssapy.pricePrediction.jointGMM import jointGMM

class targetMU(margDistPredictionAgent):

    @staticmethod       
    def type():
        return "targetMU"
            
    @staticmethod
    def SS(**kwargs):
        """
        Calculate the expected marginal price vector given marginal distributions
        over good prices. 
        """
        pricePrediction = kwargs.get('pricePrediction')
        if pricePrediction == None:
            raise KeyError("straightMU.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("straightMU.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("straightMU8 - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("straightMU8 - must specify l (target number of time slots)")
        
        if isinstance(pricePrediction, margDistSCPP):
            expectedPrices = pricePrediction(method='average')
            
        elif isinstance(pricePrediction, numpy.ndarray):
            expectedPrices = pricePrediction
            
        elif isinstance(pricePrediction, list):
            expectedPrices = numpy.asarray(pricePrediction)
            
        else:
            raise ValueError("Unknown Price Prediction Type.")
           
        return targetMV.SS( pointPricePrediction = expectedPrices,
                            bundles              = bundles,
                            valuation            = valuation,
                            l                    = l)     
        
class targetMU8(margDistPredictionAgent):
    """
    A concrete class for targetMU8
    """

    @staticmethod
    def type():
        return "targetMU8"
    
    @staticmethod
    def SS(**kwargs):        
        """
        Calculate the expected using inverse sampling method and 8 samples
        Then bid via targetMV with the resulting expected prices
        """
        
        pricePrediction = kwargs.get('pricePrediction')
        if pricePrediction == None:
            raise KeyError("targetMU8.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("targetMU8.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("targetMU8 - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("targetMU8 - must specify l (target number of time slots)")
        
        if isinstance(pricePrediction, margDistSCPP):
            expectedPrices = pricePrediction.expectedPrices(method = 'iTsample', nSamples = 8)
                   
        elif isinstance(pricePrediction, jointGMM):
            samples = pricePrediction.sample(n_samples=8)
            expectedPrices = numpy.mean(samples,0)
            
        else:
            raise ValueError("straightMU8 - Unknown price prediction type.")
        
        return targetMV.SS( pointPricePrediction = expectedPrices,
                            bundles              = bundles,
                            valuation            = valuation,
                            l                    = l)
        
    def printSummary(self, **kwargs):
        if 'expectedPrices' not in kwargs:
            
            kwargs['method']   = 'iTsample'
            kwargs['nSamples'] = 8
            
        super(targetMU8,self).printSummary(**kwargs)
        
class targetMU64(margDistPredictionAgent):
    @staticmethod
    def type():
        return "targetMU64"
    
    @staticmethod
    def SS(**kwargs):        
        """
        Calculate the expected using inverse sampling method and 8 samples
        Then bid via targetMV with the resulting expected prices
        """
        
        pricePrediction = kwargs.get('pricePrediction')
        if pricePrediction == None:
            raise KeyError("targetMU64.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("targetMU64.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("targetMU64 - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("targetMU64 - must specify l (target number of time slots)")
        
        if isinstance(pricePrediction, margDistSCPP):
            expectedPrices = pricePrediction.expectedPrices(method = 'iTsample', nSamples = 64)
                   
        elif isinstance(pricePrediction, jointGMM):
            samples = pricePrediction.sample(n_samples = 64)
            expectedPrices = numpy.mean(samples,0)
            
        else:
            raise ValueError("targetMU64 - Unknown price prediction type.")
        
        return targetMV.SS( pointPricePrediction = expectedPrices,
                            bundles              = bundles,
                            valuation            = valuation,
                            l                    = l)
        
    def printSummary(self, **kwargs):
        if 'expectedPrices' not in kwargs:
            
            kwargs['method']   = 'iTsample'
            kwargs['nSamples'] = 8
            
        super(targetMU64,self).printSummary(**kwargs)
        
class targetMU256(margDistPredictionAgent):
    @staticmethod
    def type():
        return "targetMU256"
    
    @staticmethod
    def SS(**kwargs):        
        """
        Calculate the expected using inverse sampling method and 8 samples
        Then bid via targetMV with the resulting expected prices
        """
        
        pricePrediction = kwargs.get('pricePrediction')
        if pricePrediction == None:
            raise KeyError("targetMU256.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("targetMU256.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("targetMU256 - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("targetMU256 - must specify l (target number of time slots)")
        
        if isinstance(pricePrediction, margDistSCPP):
            expectedPrices = pricePrediction.expectedPrices(method = 'iTsample', nSamples = 256)
                   
        elif isinstance(pricePrediction, jointGMM):
            samples = pricePrediction.sample(n_samples = 256)
            expectedPrices = numpy.mean(samples,0)
            
        else:
            raise ValueError("targetMU64 - Unknown price prediction type.")
        
        return targetMV.SS( pointPricePrediction = expectedPrices,
                            bundles              = bundles,
                            valuation            = valuation,
                            l                    = l)
        
    def printSummary(self, **kwargs):
        if 'expectedPrices' not in kwargs:
            
            kwargs['method']   = 'iTsample'
            kwargs['nSamples'] = 8
            
        super(targetMU256,self).printSummary(**kwargs)
    
        
        