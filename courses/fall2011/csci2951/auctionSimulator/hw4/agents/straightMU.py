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

class straightMU(margDistPredictionAgent):
       
    @staticmethod
    def type():
        return "straightMU"
    
    @staticmethod
    def SS(args={}):
        """
        Calculate the expected marginal price vector given marginal distributions
        over good prices. 
        
        We consider in the average, the price associated with a bin to be the
        bins center. The average is then calculated as summing the product 
        of the bin centers multiplied by the bin probability.
        """
        
        method = 'average'
        if 'method' in args:
            method = args['method']
        
        assert 'margDistPrediction' in args,\
            "Must specify margDistPrediction in args parameter."
            
        assert isinstance(args['margDistPrediction'],margDistSCPP) or\
                isinstance(args['margDistPrediction'],tuple),\
            "args['margDistPrediction'] must be an instance of type margDistSCPP or a python tuple."
            
        assert 'bundles' in args,\
            "Must specify bundles in args parameter."
            
        assert 'valuation' in args,\
            "Must specify the valuation of each bundle in the args parameter."
            
        assert 'l' in args,\
            "Must specify l, the target number of goods in args parameter"
            
        pricePrediction = None
        if isinstance(args['margDistPrediction'], margDistSCPP):
                        
            pricePrediction = args['margDistPrediction']
            
        elif isinstance(args['margDistPrediction'], tuple):
            
            pricePrediction = margDistSCPP(args['margDistPrediction'])
            
        else:
            # this should never happen
            raise AssertionError
        
        if method == 'average':
            expectedPrices = pricePrediction.expectedPrices()
        
        return straightMV.SS({ 'pointPricePrediction' : expectedPrices,
                               'bundles'              : args['bundles'],
                               'l'                    : args['l'],
                               'valuation'            : args['valuation'] })