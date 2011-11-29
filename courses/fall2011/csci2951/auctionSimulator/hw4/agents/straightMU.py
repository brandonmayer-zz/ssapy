"""
this is /auctionSimulator/hw4/straightMU.py

Author: Brandon Mayer
Date:   11/21/2011

Specialized agent class to replicate straightMU from Yoon and Wellman 2011.
This is just a wrapper around targetMV and accepts a price prediction distribution
and calculates the mean(s) for price prediction
"""
from margDistPredictionAgent import *

class straightMU(margDistPredictionAgent):
       
    @staticmethod
    def type():
        return "straightMU"
    
    @staticmethod
    def SS(args={}):
        pass
    
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
        