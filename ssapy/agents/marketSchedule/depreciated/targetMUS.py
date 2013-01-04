"""
this is /auctionSimulator/hw4/targetMU.py

Author: Brandon Mayer
Date:   11/21/2011

Specialized agent class to replicate targetMUS from Yoon and Wellman 2011.
This is just a wrapper around targetMVS and accepts a price prediction distribution
and calculates the mean(s) for price prediction
"""
import numpy

from margDistPredictionAgent import margDistPredictionAgent
from ssapy.pricePrediction.jointGMM import jointGMM
from ssapy.pricePrediction.margDistSCPP import margDistSCPP
from targetMVS import targetMVS

#import copy

class targetMUS(margDistPredictionAgent):

    @staticmethod        
    def type():
        return "targetMUS"
    
    @staticmethod
    def SS(**kwargs):
        """
        Calculate the expected marginal price vector given marginal distributions
        over good prices. 
        
        targetMUS assumes that "all goods outside the taget bundle
        are unavailable" (Yoon & Wellman 2011)
        """
        pricePrediction = kwargs.get('pricePrediction')
        if pricePrediction == None:
            raise KeyError("targetMUS.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("targetMUS.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("targetMUS - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("targetMUS - must specify l (target number of time slots)")
        
        if isinstance(pricePrediction, margDistSCPP):
            expectedPrices = pricePrediction(method='average')
            
        elif isinstance(pricePrediction, numpy.ndarray):
            expectedPrices = pricePrediction
            
        elif isinstance(pricePrediction, list):
            expectedPrices = numpy.asarray(pricePrediction)
            
        else:
            raise ValueError("targetMUS.SS(...) - Unknown Price Prediction Type.")
        
        return targetMVS.SS(pointPricePrediction = expectedPrices,
                             bundles             = bundles,
                             l                   = l,
                             valuation           = valuation)
        
class targetMUS8(margDistPredictionAgent):
    """
    A concrete class for targetMUS8
    """
    @staticmethod
    def type():
        return "targetMUS8"
    
    @staticmethod
    def SS(**kwargs):

        pricePrediction = kwargs.get('pricePrediction')
        if pricePrediction == None:
            raise KeyError("targetMUS8.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("targetMUS8.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("targetMUS8 - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("targetMUS8 - must specify l (target number of time slots)")
        
        if isinstance(pricePrediction, margDistSCPP):
            expectedPrices = pricePrediction.expectedPrices(method = 'iTsample', nSamples = 8)
            
        elif isinstance(pricePrediction, numpy.ndarray):
            expectedPrices = pricePrediction
                   
        elif isinstance(pricePrediction, jointGMM):
            samples = pricePrediction.sample(n_samples=8)
            expectedPrices = numpy.mean(samples,0)
            
        else:
            raise ValueError("targetMUS8 - Unknown price prediction type.")
        
        return targetMVS.SS( pointPricePrediction = expectedPrices,
                              bundles              = bundles,
                              valuation            = valuation,
                              l                    = l)
        
    def printSummary(self, **kwargs):
        
        if 'expectedPrices' not in kwargs:
            kwargs['method']   = 'iTsample'
            kwargs['nSamples'] = 8
            
        super(targetMUS8,self).printSummary(**kwargs)
        
        
class targetMUS64(margDistPredictionAgent):
    @staticmethod
    def type():
        return "targetMUS64"
    
    @staticmethod
    def SS(**kwargs):
        pricePrediction = kwargs.get('pricePrediction')
        if pricePrediction == None:
            raise KeyError("targetMUS64.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("targetMUS64.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("targetMUS64 - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("targetMUS64 - must specify l (target number of time slots)")
        
        if isinstance(pricePrediction, margDistSCPP):
            expectedPrices = pricePrediction.expectedPrices(method = 'iTsample', nSamples = 64)
            
        elif isinstance(pricePrediction, numpy.ndarray):
            expectedPrices = pricePrediction
                   
        elif isinstance(pricePrediction, jointGMM):
            samples = pricePrediction.sample(n_samples = 64)
            expectedPrices = numpy.mean(samples,0)
            
        else:
            raise ValueError("targetMUS64 - Unknown price prediction type.")
        
        return targetMVS.SS( pointPricePrediction = expectedPrices,
                              bundles              = bundles,
                              valuation            = valuation,
                              l                    = l)
    
    def printSummary(self, **kwargs):
        tkwargs = dict(kwargs)
        
        if 'expectedPrices' not in tkwargs:
            tkwargs['method']   = 'iTsample'
            tkwargs['nSamples'] = 64
            
        super(targetMUS64,self).printSummary(**tkwargs)
        
class targetMUS256(margDistPredictionAgent):
    @staticmethod
    def type():
        return "targetMUS256"
    
    @staticmethod
    def SS(**kwargs):
        pricePrediction = kwargs.get('pricePrediction')
        if pricePrediction == None:
            raise KeyError("targetMUS256.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("targetMUS256.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("targetMUS256 - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("targetMUS256 - must specify l (target number of time slots)")
        
        if isinstance(pricePrediction, margDistSCPP):
            expectedPrices = pricePrediction.expectedPrices(method = 'iTsample', nSamples = 256)
            
        elif isinstance(pricePrediction, numpy.ndarray):
            expectedPrices = pricePrediction
                   
        elif isinstance(pricePrediction, jointGMM):
            samples = pricePrediction.sample(n_samples = 256)
            expectedPrices = numpy.mean(samples,0)
            
        else:
            raise ValueError("targetMUS256 - Unknown price prediction type.")
        
        return targetMVS.SS( pointPricePrediction = expectedPrices,
                              bundles              = bundles,
                              valuation            = valuation,
                              l                    = l)
    
    def printSummary(self, **kwargs):
        tkwargs = dict(kwargs)
        
        if 'expectedPrices' not in tkwargs:
            tkwargs['method']   = 'iTsample'
            tkwargs['nSamples'] = 64
            
        super(targetMUS64,self).printSummary(**tkwargs)
        