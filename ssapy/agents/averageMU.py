"""
this is /auctionSimulator/hw4/averageMU.py

Author: Brandon Mayer
Date:   11/21/2011

Specialized agent class to replicate averageMU from Yoon and Wellman 2011.
"""

from margDistPredictionAgent import *

class averageMU(margDistPredictionAgent):
    @staticmethod       
    def type():
        return "averageMU"
    
    @staticmethod
    def SS(**kwargs):     
        
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
        
        n_samples = kwargs.get('n_samples', 8)
        
        if isinstance(pricePrediction, margDistSCPP):
            samples = pricePrediction.sample(n_samples = n_samples)
            
            
        elif isinstance(pricePrediction, jointGMM):
            samples = pricePrediction.sample(n_samples = n_samples)
        else:
            raise ValueError("Unknown Price Prediction Type.")
        
        smu_of_samples = numpy.zeros(samples.shape)
        
        for row, sample in enumerate(samples):
            smu_of_samples[row,:] = straightMV.SS( pointPricePrediction = sample,
                                                   bundles              = bundles,
                                                   valuation            = valuation,
                                                   l                    = l)
            
        avgMu = numpy.mean(smu_of_samples,0)
        return numpy.mean(avgMu)
            
class averageMU8(averageMU):
    @staticmethod
    def type():
        return "averageMU8"
    
    @staticmethod
    def SS(**kwargs):
        kwargs['n_samples'] = 8
        
        return averageMU.SS(**kwargs)
    
class averageMU64(averageMU):
    @staticmethod
    def type():
        return "averageMU64"
    
    @staticmethod
    def SS(**kwargs):
        kwargs['n_samples'] = 64
        
        return averageMU.SS(**kwargs)
    
class averageMU256(averageMU):
    @staticmethod
    def type():
        return "averageMU256"
    
    @staticmethod
    def SS(**kwargs):
        kwargs['n_samples'] = 256
        
        return averageMU.SS(**kwargs)