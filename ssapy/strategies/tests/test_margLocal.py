import os
import pickle
import unittest
import numpy

from ssapy import listBundles, msListRevenue, msRandomValueVector
from ssapy.strategies.margLocal import margLocalA, margLocalUpdate, margLocal


class test_margLocalBid(unittest.TestCase):
    def setUp(self):
        self.ppFile = os.path.realpath("./jointGmmScppHob_straightMU8_m5_n8_00013.pkl")
        with open(self.ppFile,'r') as f:
            self.pp = pickle.load(f)
            
    def test_margLocalUpdate1(self):
        """
        Updates computed by hand given:
        v = [45,20], l = 1
        p(q_1 = 20) = 0.5 
        p(q_1 = 30) = 0.5
        p(q_2 = 15) = 0.2
        p(q_2 = 20) =  0.8
        
        Under independent prices p(q_1,q_2) = p(q_1)p(q_2)
        Hence:
        p(q_1 = 20, q_2 = 15) = 0.1
        p(q_1 = 20, q_2 = 20) = 0.4
        p(q_1 = 30, q_2 = 15) = 0.1
        p(q_1 = 30, q_2 = 20) = 0.4
        
        The joint pdf is represented with 1000 samples. 
        100 samples of [20,15]
        400 samples of [20,20]
        100 samples of [30,15]
        400 samples of [30,20]
        
        Ground Truth Anwers:
        Starting at [25,25]
        1.1) b1 <- 25
        1.2) b2 <- 10
        2.1) b1 <- 45
        2.2) b2 <- 0
        3.1) b1 <- 25
        3.2) b2 <- 0
        
        Therefore, starting at [25,25] converges to [45,0] after 3 iterations
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

        bids[0] = margLocalUpdate(bundles,revenue,bids,0,samples,True)
        numpy.testing.assert_equal(bids[0], 25, "Update 1.1 Failed", True)
                
        bids[1] = margLocalUpdate(bundles,revenue,bids,1,samples,True)
        numpy.testing.assert_equal(bids[1], 10, "Update 1.2 Failed", True )
                
        bids[0] = margLocalUpdate(bundles,revenue,bids,0,samples,True)
        numpy.testing.assert_equal(bids[0], 45, "Update 2.1 Failed", True)
                
        bids[1] = margLocalUpdate(bundles,revenue,bids,1,samples,True)
        numpy.testing.assert_equal(bids[1], 0, "Update 2.2 Failed", True)
                
        bids[0] = margLocalUpdate(bundles,revenue,bids,0,samples,True)
        numpy.testing.assert_equal(bids[0], 45, "Update 3.1 Failed", True)
                
        bids[1] = margLocalUpdate(bundles,revenue,bids,1,samples,True)
        numpy.testing.assert_equal(bids[1], 0, "Update 3.2 Failed", True)
        
        #should converge after 3 iterations
        bids = numpy.asarray([25.,25.])
        
        bids, converged, itr, tol = margLocal(bundles, revenue, bids, samples, ret = 'all')
        
        numpy.testing.assert_array_equal(bids, numpy.asarray([45,0]), "margLocal bids test failed", True)
        
        numpy.testing.assert_equal(converged, True, "margLocal converged failed", True)
        
        numpy.testing.assert_equal(itr,3,"margLocal number of iterations failed.", True)
        
        numpy.testing.assert_almost_equal(tol, 0., 8, "margLocal tol failed", True)
        
       
        
#    def test_vanillia(self):
#        m = 5
#        bundles = listBundles(m)
#        v,l = msRandomValueVector(0, 50, m)
#        revenue = msListRevenue(bundles, v, l)
#        
#        print margLocalA(bundles = bundles, valuation = revenue, pricePrediction = self.pp, verbose = True)


        
if __name__ == "__main__":
    unittest.main()
        
        