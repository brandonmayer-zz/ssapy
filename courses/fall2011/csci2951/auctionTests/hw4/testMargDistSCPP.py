"""
this is /auctionTests/testPredictionIO.py

Author:    Brandon A. Mayer
Date:      11/26/2011

Just some sanity checks.
"""

from auctionSimulator.hw4.pricePrediction.marginalDistributionSCPP import *

import numpy
import unittest

class testMarginalDistributionSCPP(unittest.TestCase):
    """
    Unit test worker class
    """
    def setUp(self):
        """
        Initialize some random distributions that will act as test data for 
        Self Confirming Price Predictions.
        """
        #make some fake data
        self.m = 5
        self.randomPriceVector = numpy.random.random_integers(1,10,self.m)
        
        mu = [5,3,2,1,1]
        sigma = [.2]*self.m
        self.randomPriceDist = []
        self.randomPriceCount = []
        for good in xrange(self.m):
            randomPrices = numpy.random.normal(loc=mu[good],scale=sigma[good],size=10000)
            self.randomPriceDist.append(numpy.histogram(randomPrices,bins=range(0,51),density=True))
            
            #this is to purposely cause errors
            self.randomPriceCount.append(numpy.histogram(randomPrices,bins=range(0,51),density=False))
        #test a single distribution
        
        