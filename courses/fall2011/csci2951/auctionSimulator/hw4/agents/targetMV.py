"""
this is /auctionSimulator/hw4/targetMV.py

Author: Brandon Mayer
Date: 11/17/2011

Specialized agent class to replicate targetMV from
Yoon and Wellman (2011)
"""
from pointPredictionAgent import *

class targetMV(pointPredictionAgent):
    def __init__(self,
                 m = 5,
                 v = None,
                 l = None,
                 vmin = 1, 
                 vmax = 50,
                 pointPricePrediction = None,
                 name="Anonymous"): 
        super(targetMV,self).__init__(m = m,
                                      v = v,
                                      l = l,
                                      vmin = vmin,
                                      vmax = vmax,
                                      pointPricePrediction = pointPricePrediction,
                                      name = name)
        
    @staticmethod
    def type(self):
        return "targetMV"
    
    @staticmethod
    def SS(self,args={}):
        """
        Calculate a vector of marginal values given a price
        vector.
        """
        assert 'pointPricePrediction' in args,\
            "Must specify pointPricePrediciton in args parameter."
            
        assert 'bundles' in args,\
            "Must specify bundles in args parameter."
            
        assert 'valuation' in args,\
            "Must specify the valuation of each bundle in args parameter."
            
        assert 'l' in args,\
            "Must specify l, the target number of goods in args parameter."

        
        
        
                
        # solve acq for optimal bundle
        # size checks of parameters will be done in acq
        [optBundle, optSurplus] = simYW.acqYW(bundles=args['bundles'],
                                            valuation=args['valuation'],
                                            l=args['l'],
                                            priceVector=args['pointPricePrediction'])
            
        pricePrediction = args['pointPricePrediction']
        
        m = bundles.shape[0]
        
        marginalValueBid = []
        for idx in xrange(m):
            if optBundle[idx] == 1:
                tempPriceInf = numpy.array(pricePrediction).astype(numpy.float)
                tempPriceInf[idx] = float('inf')
                tempPriceZero = numpy.array(pricePrediction).astype(numpy.float)
                tempPriceZero[idx] = 0
                
#                [optIdxInf, optBundleInf, predictedSurplusInf] = self.acq(tempPriceInf,validate=False)
#                [optIdxZero, optBundleZero, predictedSurplusZero] = self.acq(tempPriceZero,validate=False)

                optBundleInf, predictedSurplusInf = simYW.acqYW(bundles=args['bundles'],
                                                                valuation=args['valuation'],
                                                                l=args['l'],
                                                                priceVector = tempPriceInf)
                
                optBundleZero, optSurplusZero = simYW.acqYW(bundles=args['bundles'],
                                                                valuation=args['valuation'],
                                                                l=args['l'],
                                                                priceVector = tempPriceZero)
                
                # this shouldn't happen but just in case       
                if predictedSurplusZero - predictedSurplusInf < 0:
                    marginalValueBid.append(0)
                else:
                    marginalValueBid.append(predictedSurplusZero-predictedSurplusInf)
                    
            else:
                marginalValueBid.append(0)
        
        return numpy.atleast_1d(marginalValueBid).astype('float')
    
             
    def bid(self,args={}):
        """
        Bid is a vector of prives given a vector
        of predicted point prices.
        
        Marginal Value:
            Solve acq for each good when good_i is unobtainable (price = inf)
            and when good_i is free (price = 0) and take the difference
        """
        
        if 'pointPricePrediction' in args:
            return self.SS({'pointPricePrediction':args['pointPricePrediction']})
        elif self.pricePrediction:
            return self.SS({'pointPricePrediction': self.pointPricePrediction})
        else:
            warning = "----WARNING----\n" +\
                      "auctionSimulator.hw4.agents.{0}.bid\n".format(self.type()) +\
                      "A point price prediction was not specified as an argument and " +\
                      "this instance has no stored prediction.\n"+\
                      "Agent id {0} will bid zero price for all items\n".format(self.id)
            sys.stderr.write(warning)
            return numpy.zeros(self.l)
          