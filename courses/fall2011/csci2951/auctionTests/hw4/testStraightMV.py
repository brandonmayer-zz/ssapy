"""
this is /auctionTests/testTargetPrice.py

Author:    Brandon A. Mayer
Date:      11/27/2011

Test the targetPrice agent
"""

from auctionSimulator.hw4.agents.straightMV import *

import numpy
import unittest
import tempfile

class testStraightMV(unittest.TestCase):
    """
    Unit test worker class for straighMV tests.
    """
    def test_straightMV(self):
        """
        Test basic straightMV functionality
        """
        m = 5
        
        # test the pickle constructors
        randomPointPrediction = pointSCPP(numpy.random.random_integers(1,10,m))
        
        tempFileObject = tempfile.NamedTemporaryFile('w+b', suffix='.pkl')
        
        randomPointPrediction.savePickle(tempFileObject.file)
        
        # set index to beggining of file to simulate close and re-open
        tempFileObject.file.seek(0)
        
        randomPointPrediction2 = pointSCPP()
    
        randomPointPrediction2.loadPickle(tempFileObject.file)
        
        # test that the pickle methods work
        numpy.testing.assert_equal(randomPointPrediction.data,
                                   randomPointPrediction2.data, 
                                   err_msg = 'Pickling save/load failed')
        
        myStraightMV = straightMV(pointPricePrediction = randomPointPrediction)
        
        numpy.testing.assert_equal( myStraightMV.pricePrediction.data,
                                    randomPointPrediction.data,
                                    err_msg = 'straightMV instance constructor failed.')
        
        myStraightMV.printSummary()
        
        bid = myStraightMV.bid()
        
        bid2 = myStraightMV.bid({'pointPricePrediciton':randomPointPrediction})
        
        bid3 = myStraightMV.bid({'pointPricePrediction':randomPointPrediction.data})
        
        numpy.testing.assert_equal(bid, bid2)
        
        numpy.testing.assert_equal(bid2, bid3)
        
        #test that a bid with a different instance but same parameters
        #yields expected results
        myStraightMV2 = straightMV(l=myStraightMV.l,v=myStraightMV.v,m=myStraightMV.m)
        
        bid4 = myStraightMV2.bid({'pointPricePrediction':randomPointPrediction})
        
        numpy.testing.assert_equal(bid4, bid)
        
        # test that a bid with the static strategy profile yeilds expected
        # bid
        bundles = simYW.allBundles(m)
        v = myStraightMV.v
        l = myStraightMV.l
        bid5 = straightMV.SS({'bundles':simYW.allBundles(m),
                              'valuation': myStraightMV.valuation(bundles = bundles, v = v, l = l),
                              'pointPricePrediction':randomPointPrediction2.data,
                              'l':l})
        
        numpy.testing.assert_equal(bid, bid5)
        
    
if __name__ == "__main__":
    unittest.main()