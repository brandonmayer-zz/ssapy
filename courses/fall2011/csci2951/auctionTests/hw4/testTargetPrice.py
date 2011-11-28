"""
this is /auctionTests/testTargetPrice.py

Author:    Brandon A. Mayer
Date:      11/27/2011

Test the targetPrice agent
"""
from auctionSimulator.hw4.agents.targetPrice import *

import numpy
import unittest
import tempfile

class testTargetPrice(unittest.TestCase):
    """
    Unit test worker class for targetPrice tests.
    """
    def testTargetConstructor(self):
        """
        Test the target price constructors
        """
        m = 5
               
        randomPointPrediction = pointSCPP(numpy.random.random_integers(1,10,m))
        
        myTargetPrice = targetPrice(name = "myTargetPrice",
                                    m = m,
                                    pointPricePrediction = randomPointPrediction)
        
        numpy.testing.assert_equal(randomPointPrediction.data, 
                                   myTargetPrice.pricePrediction.data, 
                                   err_msg="randomPointPrediction.data = {0} and " +\
                                           "myTargetPrice.pricePrediction.data = {1] " +\
                                           "should be equal".format(randomPointPrediction.data,
                                                                    myTargetPrice.pricePrediction.data)) 
                                   
        
        # test all the calls to super's produce the desired results
        self.assertEqual("myTargetPrice", myTargetPrice.name)
    
        self.assertEqual(m,myTargetPrice.m)
    
        #inspect via ocular method :P    
        myTargetPrice.printSummary()
        
        #test basic bid expectation
        bid = myTargetPrice.bid()
        
        bundles = simYW.allBundles(m)
        valuation = simYW.valuation(bundles=bundles, 
                                    v=myTargetPrice.v, 
                                    l=myTargetPrice.l)
        
        [optBundle, optSurplus] = simYW.acqYW(bundles,
                                            valuation,
                                            myTargetPrice.l,
                                            randomPointPrediction.data)
        
        targetBid = []
        for idx in xrange(optBundle.shape[0]):
            if optBundle[idx]:
                targetBid.append(randomPointPrediction.data[idx])
            else:
                targetBid.append(0)
        targetBid = numpy.atleast_1d(targetBid)
                
        
        numpy.testing.assert_equal(bid,targetBid)
                
if __name__ == "__main__":
    unittest.main()