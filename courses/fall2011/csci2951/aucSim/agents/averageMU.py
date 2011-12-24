"""
this is /auctionSimulator/hw4/averageMU.py

Author: Brandon Mayer
Date:   11/21/2011

Specialized agent class to replicate averageMU from Yoon and Wellman 2011.
"""

from margDistPredictionAgent import margDistPredictionAgent
#from aucSim.pricePrediction import *

class averageMU(margDistPredictionAgent):
    @staticmethod       
    def type():
        return "averageMU"
    
    @staticmethod
    def SS(**kwargs):        
        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        nSamples = kwargs.get('nSamples', 8)
                
        priceSamples = pricePrediction.iTsample(nSamples = nSamples)

        bundles = kwargs.get('bundles', simYW.allBundles(pricePrediction.m))
        
        #for each price vector, we calculate the marginal
        #value of the ith good
        avgMV = numpy.zeros(pricePrediction.m,dtype=numpy.float)
        
        for idx in xrange(priceSamples.shape[1]):
            mv = []
            for s in priceSamples:
                tempPriceInf = numpy.array(s).astype(numpy.float)
                tempPriceInf[idx] = float('inf')
                tempPriceZero = numpy.array(s)
                tempPriceZero[idx] = 0
                
                [optBundleInf, predictedSurplusInf]    = simYW.acqYW(bundles     = bundles,
                                                                     valuation   = kwargs['valuation'],
                                                                     l           = kwargs['l'],
                                                                     priceVector = tempPriceInf)
                
                [optBundleZero, predictedSurplusZero] = simYW.acqYW(bundles     = bundles,
                                                                    valuation   = kwargs['valuation'],
                                                                    l           = kwargs['l'],
                                                                    priceVector = tempPriceZero )
                
                if predictedSurplusZero - predictedSurplusInf < 0:
                    print''
                    sys.stderr.write('----WARNING----\n')
                    sys.stderr.write('averageMU8: predictedSurplusZero - predictedSurplusInf < 0 \n')
                    print ''
                    mv.append(0)
                else:
                    mv.append(predictedSurplusZero - predictedSurplusInf)
                    
            avgMV[idx]=numpy.mean(mv)
            
        return avgMV
    
class averageMU8(averageMU):
    @staticmethod
    def type():
        return "averageMU8"
    
    @staticmethod
    def SS(**kwargs):
        kwargs['nSamples'] = 8
        
        return averageMU.SS(**kwargs)
    
class averageMU64(averageMU):
    @staticmethod
    def type():
        return "averageMU64"
    
    @staticmethod
    def SS(**kwargs):
        kwargs['nSamples'] = 64
        
        return averageMU.SS(**kwargs)
    
class averageMU256(averageMU):
    @staticmethod
    def type():
        return "averageMU256"
    
    @staticmethod
    def SS(**kwargs):
        kwargs['nSamples'] = 256
        
        return averageMU.SS(**kwargs)