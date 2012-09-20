"""
this is /auctionSimulator/hw4/straightMV.py

Author: Brandon Mayer
Date: 11/17/2011

Specialized agent class to replicate straightMV from
Yoon and Wellman (2011)
"""
#from auctionSimulator.hw4.agents.pointPredictionAgent import *
from pointPredictionAgent import *

class straightMV(pointPredictionAgent):
    """
    straightMV bids marginal values for all goods.
    """
    @staticmethod
    def type():
        return "straightMV"
    
    @staticmethod
    def SS(**kwargs):
        """
        Calculate the marginal values of all goods for auction
        given the predicted prices.
        
        NOTE:
            Bid on all available goods, don't solve acq for overall best bundle.
            
        Parameters:
            pointPricePrediction     A point price prediction
            bundles                  The available bundles to bid on
            valuation                A vector of valuations (one valuation per bundle)
            l                        The target number of goods
        """

        assert 'pointPricePrediction' in kwargs,\
            "Must specify pointPricePrediction in kwargs parameter."
            
        assert isinstance(kwargs['pointPricePrediction'],pointSCPP) or\
                isinstance(kwargs['pointPricePrediction'], numpy.ndarray),\
               "kwargs['pointPricePrediction'] must be either a pointSCPP or numpy.ndarray"
            
        assert 'bundles' in kwargs,\
            "Must specify bundles in kwargs parameter."
            
        assert 'valuation' in kwargs,\
            "Must specify the valuation of each bundle in the kwargs parameter."
            
        assert 'l' in kwargs,\
            "Must specify l, the target number of goods in kwargs parameter."
            
        if isinstance(kwargs['pointPricePrediction'], pointSCPP):
                        
            pricePrediction = kwargs['pointPricePrediction'].data
            
        elif isinstance(kwargs['pointPricePrediction'],numpy.ndarray):
            
            pricePrediction = numpy.atleast_1d(kwargs['pointPricePrediction'])
            
        else:
            # this should never happen
            pricePrediction = None
            raise AssertionError
        
        marginalValueBid = []
        for idx in xrange(kwargs['bundles'].shape[1]):
            tempPriceInf = numpy.array(pricePrediction).astype(numpy.float)
            tempPriceInf[idx] = float('inf')
            tempPriceZero = numpy.array(pricePrediction)
            tempPriceZero[idx] = 0 
            
            optBundleInf, predictedSurplusInf = simYW.acqYW(bundles     = kwargs['bundles'],
                                                            valuation   = kwargs['valuation'],
                                                            l           = kwargs['l'],
                                                            priceVector = tempPriceInf)
            
            optBundleZero, predictedSurplusZero = simYW.acqYW(bundles     = kwargs['bundles'],
                                                              valuation   = kwargs['valuation'],
                                                              l           = kwargs['l'], 
                                                              priceVector = tempPriceZero)
                
            #this shouldn't happend but just in case.
            if predictedSurplusZero - predictedSurplusInf < 0:
                marginalValueBid.append(0)
            else:
                marginalValueBid.append(predictedSurplusZero - predictedSurplusInf)
            
        return numpy.atleast_1d(marginalValueBid).astype('float')
        
            