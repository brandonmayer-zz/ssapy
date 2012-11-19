import copy
import unittest

from ssapy import dok_hist
from ssapy.pricePrediction.dok_hist import expected_cost

class test_dok_hist(unittest.TestCase):
    def setUp(self):
        hist = dok_hist(m = 2)
        hist.upcount([0, 0], 10)
        hist.upcount([50,50], 10)
        
        hist.upcount([10,14], 5)
        hist.upcount([11,20], 7)
               
    def test_marginal(self):
        joint_hist = dok_hist(m=2)
        joint_hist.upcount([1,1],10)
        joint_hist.upcount([2,2],10)
        
        marg_hist = joint_hist.marginal(0)
        
        self.assertEqual(marg_hist.density(1), 0.5, "marg_hist.density(1) != 0.5")
        self.assertEqual(marg_hist.density(2), 0.5, "marg_hist.density(2) != 0.5")
        
        for i in xrange(3,50):
            self.assertEqual(marg_hist.density(i), 0.0, "marg_hist.density({0}) != .5".format(i))
            
            
        joint_hist = dok_hist(m=2)        
        joint_hist.upcount([1,1],0.5)
        joint_hist.upcount([1,2],0.1)
        joint_hist.upcount([2,1],0.2)
        joint_hist.upcount([2,2],0.2)
        
        marg_hist = joint_hist.marginal(0)
        
        self.assertAlmostEqual(marg_hist.density(1), 0.6, 
                         "marg_hist.density(1) = {0} != 0.6".\
                         format(marg_hist.density(1)))
        
        
        self.assertAlmostEqual(marg_hist.density(2), 0.4)

        marg_hist = joint_hist.marginal(1)
        
        self.assertAlmostEqual(marg_hist.density(1), 0.7)
        
        self.assertAlmostEqual(marg_hist.density(2),0.3)
        
    def test_marginal_expected_cost(self):
        marg_hist = dok_hist(m=1)
        
        marg_hist.upcount(0, 50)
        marg_hist.upcount(.5, 25)
        marg_hist.upcount(1.5,25)
        
        bid = 1.5
        
        ec = expected_cost(marg_hist,bid)
               
        self.assertAlmostEqual(ec, 0.28125)
        
        ec = expected_cost(marg_hist,0)
        
        self.assertAlmostEqual(ec,0.0)
        
    def test_expected_cost(self):
        hist = dok_hist(m=2)
        
        hist.set([0,30],0.5)
        hist.set([30,0],0.5)
        
        
if __name__ == '__main__':
    unittest.main()
        
