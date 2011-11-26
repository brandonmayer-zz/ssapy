"""
this is /auctionTests/testPredictionIO.py

Author:    Brandon A. Mayer
Date:      11/26/2011

Just some IO sanity checks.
"""
from auctionSimulator.hw4.pricePrediction.marginalDistributionSCPP import *
from auctionSimulator.hw4.pricePrediction.pointSCPP import *

import numpy
import unittest
import tempfile
class TestPredictionIO(unittest.TestCase):
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
        for good in xrange(self.m):
            randomPrices = numpy.random.normal(loc=mu[good],scale=sigma[good],size=10000)
            self.randomPriceDist.append(numpy.histogram(randomPrices,bins=range(0,51),density=True))
            
        #make some temporary files
        self.pointFileObject = tempfile.NamedTemporaryFile('w+b',suffix='.pkl')
        self.distFileObject = tempfile.NamedTemporaryFile('w+b',suffix='.pkl') 
        
    def test_io(self):
        
        # create the prediction instance wrappers
        pointPrediction = pointSCPP(self.randomPriceVector)
        distPrediction  = marginalDistributionSCPP(self.randomPriceDist)
                
        # save them to temp files
        pointPrediction.savePickle(self.pointFileObject.file)
        distPrediction.savePickle(self.distFileObject.file)
        
        #move to begginning for reading
        self.pointFileObject.file.seek(0)
        self.distFileObject.file.seek(0)
        
        # reload the pickled instances
        reloadedPointPrediction = pickle.load(self.pointFileObject)
        reloadedDistPrediction = pickle.load(self.distFileObject)
        
        # check the reloaded point prediction is the correct class instance
        self.assertIsInstance(reloadedPointPrediction, pointSCPP)
        
        # check the reloaded distribution prediction is the correct class instance
        self.assertIsInstance(reloadedDistPrediction, marginalDistributionSCPP)
        
        # check the reloaded distribution represents marginal distributions over the correct
        # number of goods
        self.assertEqual( len(reloadedDistPrediction.data), self.m )
        
        # check the reloaded and original distribution instances have the same 
        # number of distributions
        self.assertEqual( len(reloadedDistPrediction.data), len(distPrediction.data) )
        
        # check the reloaded and original price vectors are of the same size
        self.assertEqual( reloadedPointPrediction.data.shape, pointPrediction.data.shape )
        
         
        # check all datum are approximatly (to decimal places) the same for the reloaded point price prediction            
        self.assertEqual( list(reloadedPointPrediction.data), list(pointPrediction.data) )
        
        # loop over all marginal distributions for goods
        for idx in xrange(len(reloadedDistPrediction.data)):
            histR, binEdgesR = reloadedDistPrediction.data[idx]
            histO, binEdgesO = distPrediction.data[idx]
            
            # test that the reloaded and original histogram count arrays have the same shape
            self.assertEqual(histR.shape,histO.shape)
            
            # test that the reloaded and original histogram counts have the same data
            self.assertEqual(list(histR), list(histO))
            
            # test that the reloaded and original bin edge arrays have the same data
            self.assertEqual(list(binEdgesR), list(binEdgesO))
   
if __name__ == "__main__":
    unittest.main()