import unittest

from ssapy import dokHist

from ssapy.pricePrediction.dokHist import expected_cost, \
    prob_win_given_bid, expected_utility
    
    
class test_dokHist(unittest.TestCase):
    def setUp(self):
        hist = dokHist(m = 2)
        hist.upcount([0, 0], 10)
        hist.upcount([50,50], 10)
        
        hist.upcount([10,14], 5)
        hist.upcount([11,20], 7)
               
    def test_marginal(self):
        joint_hist = dokHist(m=2)
        joint_hist.upcount([1,1],10)
        joint_hist.upcount([2,2],10)
        
        marg_hist = joint_hist.marginal(0)
        
        self.assertEqual(marg_hist.density(1), 0.5, "marg_hist.density(1) != 0.5")
        self.assertEqual(marg_hist.density(2), 0.5, "marg_hist.density(2) != 0.5")
        
        for i in xrange(3,50):
            self.assertEqual(marg_hist.density(i), 0.0, "marg_hist.density({0}) != .5".format(i))
            
            
        joint_hist = dokHist(m=2)        
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
        marg_hist = dokHist(m=1)
        
        marg_hist.upcount(0, 50)
        marg_hist.upcount(.5, 25)
        marg_hist.upcount(1.5,25)
        
        bid = 1.5
        
        ec = expected_cost(marg_hist,bid)
               
        self.assertAlmostEqual(ec, 0.28125)
        
        ec = expected_cost(marg_hist,0)
        
        self.assertAlmostEqual(ec,0.0)
        
    def test_expected_cost(self):
        hist = dokHist(m=2, isdensity=True)
        
        hist.set([0,30],0.5)
        hist.set([30,0],0.5)
        
        bid = [25,25]
        
        ec = expected_cost(hist,bid)
        
        self.assertAlmostEqual(ec,0.0)
        
        bid = [31,31]
        
        ec = expected_cost(hist,bid)
        
        self.assertAlmostEqual(ec, 29.5)
        
    def test_prob_win_given_bid(self):
        hist = dokHist(m=2, isdensity=True)
        
        hist.set([2.5,2.5],.25)
        hist.set([5.5,1.5],.75)
        
        bid = [2.5,2.5]
        
        pwin = {}
        
        sum = 0.0
        for i in [0,1]:
            for j in [0,1]:
                pwin[(i,j)] = prob_win_given_bid(hist,[i,j],bid)
                sum+=pwin[(i,j)]
                
        self.assertAlmostEqual(pwin[(0,0)], 1./16)
        self.assertAlmostEqual(pwin[(1,0)], 1./16)
        self.assertAlmostEqual(pwin[(0,1)], 13./16)
        self.assertAlmostEqual(pwin[(1,1)], 1./16)
        self.assertAlmostEqual(sum,1.0)
        
        del hist
        hist = dokHist(m=2, isdensity = True)
        hist.set([2.5,2.5],0.25)
        hist.set([5.5,1.5],0.25)
        hist.set([4.5,4.5],0.5)
        bid = [4,3]
        pwin = {}
        sum= 0.0
        for i in [0,1]:
            for j in [0,1]:
                pwin[(i,j)] = prob_win_given_bid(hist,[i,j],bid)
                sum += pwin[(i,j)]
                
        self.assertAlmostEqual(pwin[(0,0)], 0.5)
        self.assertAlmostEqual(pwin[(0,1)], 0.25)
        self.assertAlmostEqual(pwin[(1,0)], 0.0)
        self.assertAlmostEqual(pwin[(1,1)], 0.25)
        self.assertAlmostEqual(sum,1.0)
        
#    def test_expected_utility(self):
#        hist = dok_hist(m=2, isdensity = True)
#        hist.set([0,30],0.5)
#        hist.set([30,0],0.5)
#        import ssapy
#        import numpy
#        
#        bundles = ssapy.allBundles(2)
#        valuation = numpy.zeros(bundles.shape[0])
#        valuation[-1] = 50
#        
#        bids = [25,25]
#        eu = expected_utility(hist, bundles, valuation, bids)
#        
#        print 'eu = {0}'.format(eu)
#        self.assertAlmostEqual(eu, 0.0)
#        
#        bids = [31,25]
#        ec = expected_cost(hist,bids)
#        print 'ec = {0}'.format(ec)
#        eu = expected_utility(hist,bundles,valuation,bids)
#        print 'eu = {0}'.format(eu)
#        self.assertAlmostEqual(eu,10)
        
if __name__ == '__main__':
    unittest.main()
    