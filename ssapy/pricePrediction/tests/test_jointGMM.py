import unittest
import numpy

from ssapy.pricePrediction.jointGMM import jointGMM, expectedSurplus_
from ssapy import listBundles, msListRevenue

class test_jointGMM(unittest.TestCase):
    def test_expectedSurplus(self):
        """
        [20,15] -> (45 - 35)*.1
        [20,20] -> (45 -40)*.4
        [30,15] -> (20 - 5)*.1
        [30,20] -> (20 - 20)*.4
        Expected Surplus = 3.5
        """
        samples = numpy.zeros((1000,2))
        samples[:100,:] = numpy.asarray([20,15])
        samples[100:500,:] = numpy.asarray([20,20])
        samples[500:600,:] = numpy.asarray([30,15])
        samples[600:,:] = numpy.asarray([30,20])
        
        m=2
        l = 1
        v = [45,20]
        bundles = listBundles(m)
        revenue = msListRevenue(bundles, v, l)
        bids = numpy.asarray([25.,25.])
        
        bundleRevenueDict = {}
        for b,r in zip(bundles,revenue):
            bundleRevenueDict[tuple(b)] = r
        
        numpy.testing.assert_equal(expectedSurplus_(bundleRevenueDict, bids, samples), 
                                   3.5,'test_expetedSurplus failed.',True)
        

if __name__ == "__main__":
    unittest.main()