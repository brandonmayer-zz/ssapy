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
        
        bid = myTargetPrice.bid()
        
        bundles = simYW.allBundles(m)
        valuation = simYW.valuation(bundles=bundles, 
                                    v=myTargetPrice.v, 
                                    l=myTargetPrice.l)
        [optBundle, optSurplus] = simYW.acq(bundles,
                                            valuation,
                                            myTargetPrice.l,
                                            randomPointPrediction.data)
        
        
        
        
        

if __name__ == "__main__":
    unittest.main()