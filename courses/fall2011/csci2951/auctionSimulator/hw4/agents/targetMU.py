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

class targetMU(margDistPredictionAgent):

    @staticmethod       
    def type():
        return "targetMU"
            
    @staticmethod
    def SS(args={}):
        """
        Calculate the expected marginal price vector given marginal distributions
        over good prices. 
        """
        pricePrediction = margDistPredictionAgent.SS(args=args)
                                                     
        expectedPrices = None
        method = 'average'
        
        if 'method' in args:
            method = args['method']
            
        if method == 'average':
            
            expectedPrices = pricePrediction.expectedPrices()
            
        elif method == 'iTsample':
            
            nSamples = 8
            
            if 'nSamples' in args:
                nSamples = args['nSamples']
            
            expectedPrices = pricePrediciton.expectedPrices({'method'   : 'iTsample',
                                                             'nSamples' : nSamples})
        else:
            print '----ERROR----'
            print 'targetMU.SS'
            print 'Unkown method for calculating expected prices'
            raise AssertionError
        
        return targetMV.SS({'pointPricePrediction' : expectedPrices,
                            'bundles'              : args['bundles'],
                            'l'                    : args['l'],
                            'valuation'            : args['valuation']})
        
            
#    def SS(self,args={}):
#        """
#        Calculate the expected marginal price vector given marginal distributions
#        over good prices. 
#        
#        We consider in the average, the price associated with a bin to be the
#        bins center. The average is then calculated as summing the product 
#        of the bin centers multiplied by the bin probability.
#        """
#        
#        method = 'average'
#        if 'method' in args:
#            method = args['method']
#        
#        assert 'margDistPrediction' in args,\
#            "Must specify margDistPrediction in args parameter."
#            
#        assert isinstance(args['margDistPrediction'],margDistSCPP) or\
#                isinstance(args['margDistPrediction'],tuple),\
#            "args['margDistPrediction'] must be an instance of type margDistSCPP or a python tuple."
#            
#        assert 'bundles' in args,\
#            "Must specify bundles in args parameter."
#            
#        assert 'valuation' in args,\
#            "Must specify the valuation of each bundle in the args parameter."
#            
#        assert 'l' in args,\
#            "Must specify l, the target number of goods in args parameter"
#            
#            
#        #AGENT SPECIFIC LOGIC
#        
#        marginalAverages = []
#        if method == 'average':
#            for hist, binEdges in args['distributionPricePrediction']:
#                #calculate the average for each marginal good
#                marginalAverages.append(self.centerBinAvgFromHist(hist=hist,binEdges=binEdges))
#                        
#            marginalAverages = numpy.atleast_1d(marginalAverages)
#            
#            if marginalAverages.shape[0] != self.m:
#                warning = "----WARNING----\n"+\
#                      "auctionSimulator.hw4.agents.targetMU.SS()\n" +\
#                      "Calculated point vector has the wrong size.\n" +\
#                      "Returning a bid of all zeros."
#                sys.stderr.write(warning)
#                return numpy.zeros(self.m)
#        else:
#            warning = "----WARNING----\n"+\
#                      "auctionSimulator.hw4.agents.targetMU.SS()\n" +\
#                      "unknown method specified for extracing point prediction from distribution.\n" +\
#                      "Returning a bid of all zeros."
#            sys.stderr.write(warning)
#            return numpy.zeros(self.m)
#        
#        # now that we have a point price prediction from the distribution,
#        # bid as if we were targetMV. We can do this by just calling and
#        # returning the parent bidding strategy profile
#        return super(targetMU,self).SS({'pointPricePrediction':marginalAverages})
                
                