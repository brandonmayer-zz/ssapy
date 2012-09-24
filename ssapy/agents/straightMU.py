"""
this is /auctionSimulator/hw4/agents/straightMU.py

Author: Brandon Mayer
Date:   11/21/2011

Specialized agent class to replicate straightMU from Yoon and Wellman 2011.
This is just a wrapper around targetMV and accepts a price prediction distribution
and calculates the mean(s) for price prediction
"""
import numpy

from margDistPredictionAgent import margDistPredictionAgent
from ssapy.agents.straightMV import straightMV
from ssapy.pricePrediction.margDistSCPP import margDistSCPP
from ssapy.pricePrediction.jointGMM import jointGMM

import copy

class straightMU(margDistPredictionAgent):
    def __init__(self,**kwargs):
        super(straightMU,self).__init__(**kwargs)
                
    @staticmethod
    def type():
        return "straightMU"
    
    @staticmethod
    def SS(**kwargs):
        """
        Calculate the expected marginal price vector given marginal distributions
        over good prices. 
        
        For the base strategy straightMU.SS(...)
        the required inputs are:
            pricePrediction
            bundles
            valuation
            l
        
        pricePrediction may be a margDistSCPP instance, in which case the expected 
        expected price vector will be calculated by summing the product 
        of the bin centers multiplied by the bin probability.
        
        pricePrediction may be a numpy.ndarray with shape (m,1) or a python list
        in specifying the expected price vector. This will then be used to call straightMV
        """
        
        pricePrediction = kwargs.get('pricePrediction')
        if pricePrediction == None:
            raise KeyError("straightMU.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("straightMU.SS(...) - must specify bundles")
                
        # a list of scalar valuations
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
        
        return straightMV.SS(pointPricePrediction = expectedPrices,
                             bundles             = bundles,
                             l                   = l,
                             valuation           = valuation)
               
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
        
        pricePrediction = kwargs.get('pricePrediction')
        if pricePrediction == None:
            raise KeyError("straightMU8.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("straightMU8.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("straightMU8 - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("straightMU8 - must specify l (target number of time slots)")
        
        if isinstance(pricePrediction, margDistSCPP):
            expectedPrices = pricePrediction.expectedPrices(method = 'iTsample', nSamples = 8)
                   
        elif isinstance(pricePrediction, jointGMM):
            samples = pricePrediction.sample(n_samples=8)
            expectedPrices = numpy.mean(samples,0)
            
        else:
            raise ValueError("straightMU8 - Unknown price prediction type.")
        
        return straightMV.SS( pointPricePrediction = expectedPrices,
                              bundles              = bundles,
                              valuation            = valuation,
                              l                    = l)
        
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
        
        """
        Calculate the expected using inverse sampling method and 8 samples
        Then bid via straightMV with the resulting expected prices
        """
        pricePrediction = kwargs.get('pricePrediction')
        if pricePrediction == None:
            raise KeyError("straightMU8.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("straightMU8.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("straightMU8 - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("straightMU8 - must specify l (target number of time slots)")
        
        if isinstance(pricePrediction, margDistSCPP):
            expectedPrices = pricePrediction.expectedPrices(method = 'iTsample', nSamples = 64)
                   
        elif isinstance(pricePrediction, jointGMM):
            samples = pricePrediction.sample(n_samples = 64)
            expectedPrices = numpy.mean(samples,0)
            
        else:
            raise ValueError("straightMU64 - Unknown price prediction type.")
        
        return straightMV.SS( pointPricePrediction = expectedPrices,
                              bundles              = bundles,
                              valuation            = valuation,
                              l                    = l)
                
        
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
        """
        Calculate the expected using inverse sampling method and 8 samples
        Then bid via straightMV with the resulting expected prices
        """
        
        pricePrediction = kwargs.get('pricePrediction')
        if pricePrediction == None:
            raise KeyError("straightMU8.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("straightMU8.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("straightMU8 - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("straightMU8 - must specify l (target number of time slots)")
        
        if isinstance(pricePrediction, margDistSCPP):
            expectedPrices = pricePrediction.expectedPrices(method = 'iTsample', nSamples = 256)
                   
        elif isinstance(pricePrediction, jointGMM):
            samples = pricePrediction.sample(n_samples = 256)
            expectedPrices = numpy.mean(samples,0)
            
        else:
            raise ValueError("straightMU64 - Unknown price prediction type.")
        
        return straightMV.SS( pointPricePrediction = expectedPrices,
                              bundles              = bundles,
                              valuation            = valuation,
                              l                    = l)
        
    def printSummary(self,**kwargs):
        tkwargs = copy.deepcopy(kwargs)
        if 'expectedPrices' not in kwargs:
            
            tkwargs['method']   = 'iTsample'
            tkwargs['nSamples'] = 256
            
        super(straightMU256,self).printSummary(**tkwargs)