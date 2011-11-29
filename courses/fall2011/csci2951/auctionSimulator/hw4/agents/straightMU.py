"""
this is /auctionSimulator/hw4/straightMU.py

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
            
        assert isinstance(args['margDistPrediciton'],margDistSCPP) or\
                isinstance(args['margDistPrediction'],tuple),\
            "args['margDistPrediction'] must be an instance of type margDistSCPP or a python tuple."
            
        assert 'bundles' in args,\
            "Must specify bundles in args parameter."
            
        assert 'valuation' in args,\
            "Must specify the valuation of each bundle in the args parameter."
            
        assert 'l' in args,\
            "Must specify l, the target number of goods in args parameter"
            
        if isinstance(args['margDistPrediciton'], margDistSCPP):
                        
            pricePrediction = args['margDistSCPP']
            
        elif isinstance(args['margDistPrediciton'], tuple):
            
            pricePrediction = margDistSCPP(args['margDistPrediciton'])
            
        else:
            # this should never happen
            pricePrediction = None
            raise AssertionError
        
        if method == 'average':
            expectedPrices = pricePrediciton.expectedPrices()
        
        return straightMV.SS({ 'pointPricePrediction' : expectedPrices,
                               'bundles'              : args['bundles'],
                               'l'                    : args['l'],
                               'valuation'            : args['valuation'] })
                              
    
#    def SS(self,args={'method':'average'}):
#        """
#        Calculate the expected marginal price vector given marginal distributions
#        over good prices. 
#        
#        We consider in the average, the price associated with a bin to be the
#        bins center. The average is then calculated as summing the product 
#        of the bin centers multiplied by the bin probability.
#        """
#        if 'method' in args:
#            method = args['method']
#        else:
#            method = 'average'
#            
#        if not 'distributionPricePrediction' in args:
#            return numpy.zeros(self.m)
#        
#        marginalAverages = []
#        
#        if method == 'average':
#            marginalAverages = self.pointExpectedValFromDist(args['distributionPricePrediction'])
#        
#            if marginalAverages.shape[0] != self.m:
#                    warning = "----WARNING----\n"+\
#                          "auctionSimulator.hw4.agents.targetMUS.SS()\n" +\
#                          "Calculated point vector has the wrong size.\n" +\
#                          "Returning a bid of all zeros."
#                    sys.stderr.write(warning)
#                    return numpy.zeros(self.m)
#        else:
#            warning = "----WARNING----\n"+\
#                      "auctionSimulator.hw4.agents.targetMUS.SS()\n" +\
#                      "unknown method specified for extracing point prediction from distribution.\n" +\
#                      "Returning a bid of all zeros.\n"
#            sys.stderr.write(warning)
#            return numpy.zeros(self.m)
#                
#        return super(straightMU,self).SS({'pointPricePrediction':marginalAverages})
        