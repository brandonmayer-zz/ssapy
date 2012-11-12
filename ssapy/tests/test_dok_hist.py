import copy
import unittest

from ssapy import dok_hist

class test_dok_hist(unittest.TestCase):
    def setUp(self):
        hist = dok_hist(m = 2)
        hist.upcount([0, 0], 10)
        hist.upcount([50,50], 10)
        
        hist.upcount([10,14], 5)
        hist.upcount([11,20], 7)
        
    def test_normalize(self):
        hist_1d = dok_hist(m = 1)
        hist_1d.upcount(10, 5)
        hist_1d.upcount(23, 10)
        hist_1d.upcount(48.6, 20)
        
        gt_norm_discrete = 35
        
        norm_discrete = hist_1d.norm_constant('discrete')
        
        self.assertEqual(gt_norm_discrete, norm_discrete)
        
        hist_copy = copy.deepcopy(hist_1d)
        hist_copy.normalize()
        
        self.assertEqual( hist_copy.counts(10), 5.0/35 )
        self.assertEqual( hist_copy.counts(23), 10.0/35)
        self.assertEqual( hist_copy.counts(48.6), 20.0/35)
        
if __name__ == '__main__':
    unittest.main()
        
