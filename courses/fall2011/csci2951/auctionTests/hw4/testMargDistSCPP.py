"""
this is /auctionTests/testPredictionIO.py

Author:    Brandon A. Mayer
Date:      11/26/2011

Just some sanity checks.
"""

from auctionSimulator.hw4.pricePrediction.margDistSCPP import *

import numpy
import unittest

class testMargDistSCPP(unittest.TestCase):
    """
    A quick unit test to check the validation and storage proceedures of self confirming
    marginal distributions for price prediction. 
    """
    def setUp(self):
        """
        Initialize some random distributions that will act as test data for 
        Self Confirming Price Predictions.
        """
        #make some fake data
        self.m = 5
        self.randomPriceVector = numpy.random.random_integers(1,10,self.m)
        
        self.mu = [5,3,2,1,1]
        self.sigma = [.2]*self.m
        self.randomPriceDist = []
        self.randomPriceCount = []
        for good in xrange(self.m):
            randomPrices = numpy.random.normal(loc=self.mu[good],scale=self.sigma[good],size=10000)
            self.randomPriceDist.append(numpy.histogram(randomPrices,bins=range(0,51),density=True))
        #test a single distribution
        
    def test_constructors(self):
        
        singleConstructor = margDistSCPP(self.randomPriceDist[0])
        
        self.assertEqual(singleConstructor.m, 1, 
                         msg = "singleConstructor.m = {0} not 1".format(singleConstructor.m))
        
        numpy.testing.assert_allclose(singleConstructor.data[0], self.randomPriceDist[0][0])
        numpy.testing.assert_allclose(singleConstructor.data[1], self.randomPriceDist[0][1])
        
        #create empty data then use setPricePrediciton
        singleEmpty = margDistSCPP()
        singleEmpty.setPricePrediction(self.randomPriceDist[0])
                
        self.assertEqual(singleEmpty.m ,1)
        
        numpy.testing.assert_allclose(singleEmpty.data[0], self.randomPriceDist[0][0])
        numpy.testing.assert_allclose(singleEmpty.data[1], self.randomPriceDist[0][1])
        
        multiConstructor = margDistSCPP(self.randomPriceDist)
        
        self.assertEqual(multiConstructor.m, 
                         self.m,
                         msg = "multiConstructor.m = {0}, not self.m = {1}".format(multiConstructor.m,self.m) )

        for idx in xrange(len(self.randomPriceDist)):
            numpy.testing.assert_allclose(multiConstructor.data[idx][0], self.randomPriceDist[idx][0])
            numpy.testing.assert_allclose(multiConstructor.data[idx][1], self.randomPriceDist[idx][1])
            
        multiEmpty = margDistSCPP()
        
        multiEmpty.setPricePrediction(self.randomPriceDist)
        
        self.assertEqual(multiEmpty.m,
                         self.m,
                         msg = "multiEmpty.m = {0}, not self.m = {1}".format(multiEmpty.m,self.m))
        
        for idx in xrange(len(self.randomPriceDist)):
            numpy.testing.assert_allclose(multiEmpty.data[idx][0], self.randomPriceDist[idx][0])
            numpy.testing.assert_allclose(multiEmpty.data[idx][1], self.randomPriceDist[idx][1])
            
        expectedPriceVector = multiEmpty.expectedPrices()
        
        print ''
        print 'Expected Prices = {0}'.format(expectedPriceVector)  
        print ''
        
        #due to the random nature of the data, this may fail
        #every once in a while but it should pass most of the time
        #especially at the low accuracy
        numpy.testing.assert_almost_equal( expectedPriceVector,
                                           self.mu,
                                           decimal = 2 )
                                       
        
        #doing ok if we reach here w/o an exception
        return True
        
if __name__ == "__main__":
    unittest.main()