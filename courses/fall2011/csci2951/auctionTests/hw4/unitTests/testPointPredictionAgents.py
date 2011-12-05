"""
this is /auctionTests/hw4/testPointPredicitonAgents.py
Author:    Brandon A. Mayer
Date:      11/28/2011

Test the point prediction agents
"""

from auctionSimulator.hw4.agents.baselineBidder import *
from auctionSimulator.hw4.agents.targetPrice import *
from auctionSimulator.hw4.agents.straightMV import *
from auctionSimulator.hw4.agents.targetMV import *
from auctionSimulator.hw4.agents.targetMVS import *

import numpy
import unittest
import tempfile

class testPointPredictionAgents(unittest.TestCase):
    """
    Unit test worker class for prediction agents
    """
    def test_baselineBidderBasics(self):
        """
        Test the general framework of the baselineBidder
        """
        m = 5
        
        name = "myBaselineBidder"
        
        myBaselineBidder = baselineBidder(m=5,name=name)
        
        print '\n'
        #"ocular method"
        myBaselineBidder.printSummary()
        print '\n'
        
        #check the name is passed down the constructors correctly
        self.assertEqual(name,myBaselineBidder.name)
        
        self.assertEqual(m, myBaselineBidder.m)
        
        self.assertEqual(myBaselineBidder.type(), "baselineBidder")
        
    def test_targetPrice(self):
        """
        Test the targetPrice
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
                                   
        print '\n'
        myTargetPrice.printSummary()
        print '\n'
        # test all the calls to super produce the desired results
        self.assertEqual("myTargetPrice", myTargetPrice.name)
    
        self.assertEqual(m,myTargetPrice.m)
        
        self.assertEqual(myTargetPrice.type(), "targetPrice")
    
        #inspect via ocular method :P    
        
        
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
        print '\n'
        myStraightMV.printSummary()
        print '\n'
        
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
        
    def test_targetMV(self):
        """
        Test basic targetMV functionality
        """
        m = 5
        
        randomPointPrediction = pointSCPP(numpy.random.random_integers(1,10,m))
        
        myTargetMV = targetMV(pointPricePrediction = randomPointPrediction)
        
        numpy.testing.assert_equal(myTargetMV.pricePrediction.data,
                                   randomPointPrediction.data)
        print '\n'
        myTargetMV.printSummary()
        print '\n'
        
        bid = myTargetMV.bid()
        
        bundles = simYW.allBundles(m)
        
        v = myTargetMV.v
        
        l = myTargetMV.l
        
        valuation = targetMV.valuation(bundles, v, l)
        
        bid2 = targetMV.SS({'pointPricePrediction':randomPointPrediction.data,
                            'valuation':valuation,
                            'l':l,
                            'bundles':bundles})
        
        numpy.testing.assert_equal(bid,bid2)
        
    def test_targetMVS(self):
        """
        Test basic targetMV functionality
        """
        m = 5
        
        randomPointPrediction = pointSCPP(numpy.random.random_integers(1,10,m))
        
        myTargetMVS = targetMVS()
        
        bid = myTargetMVS.bid({'pointPricePrediction':randomPointPrediction})
        
        bid2 = myTargetMVS.bid({'pointPricePrediction':randomPointPrediction.data})
        
        numpy.testing.assert_equal(bid,bid2)
        
        myTargetMVS.printSummary({'pointPricePrediction':randomPointPrediction})
        
        
        
if __name__ == "__main__":
    unittest.main()