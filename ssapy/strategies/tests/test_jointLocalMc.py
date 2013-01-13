import unittest
import numpy

from ssapy.strategies.jointLocal import jointLocalMc, jointLocalUpdateMc
from ssapy import listBundles, msListRevenue

class test_jointLocalMc(unittest.TestCase):
    def test_jointLocalMc1(self):
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
        
        bids[0] = jointLocalUpdateMc(bundles,revenue,bids,0,samples,True)
        print bids
        numpy.testing.assert_equal(bids[0], 25, "Update 1.1 Failed", True)
                
        bids[1] = jointLocalUpdateMc(bundles,revenue,bids,1,samples,True)
        print bids
        numpy.testing.assert_equal(bids[1], 10, "Update 1.2 Failed", True )
                
        bids[0] = jointLocalUpdateMc(bundles,revenue,bids,0,samples,True)
        print bids
        numpy.testing.assert_equal(bids[0], 45, "Update 2.1 Failed", True)
                
        bids[1] = jointLocalUpdateMc(bundles,revenue,bids,1,samples,True)
        print bids
        numpy.testing.assert_equal(bids[1], 0, "Update 2.2 Failed", True)
                
        bids[0] = jointLocalUpdateMc(bundles,revenue,bids,0,samples,True)
        print bids
        numpy.testing.assert_equal(bids[0], 45, "Update 3.1 Failed", True)
                
        bids[1] = jointLocalUpdateMc(bundles,revenue,bids,1,samples,True)
        print bids
        numpy.testing.assert_equal(bids[1], 0, "Update 3.2 Failed", True)
        
        bids = numpy.asarray([25.,25.])
        bids, converged, itr, tol = jointLocalMc(bundles, revenue, bids, samples, verbose=True,ret='all')
        print bids
        print converged
        print itr
        print tol
        
if __name__ == "__main__":
    unittest.main()  