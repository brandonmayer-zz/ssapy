import unittest
import numpy

from ssapy.strategies.targetPrice import targetPrice
from ssapy import listBundles, msListRevenue

class test_targetPrice(unittest.TestCase):
    def test1(self):
        pp = [5,5]
        l = 1
        v = [20,10]
        bundles = listBundles(2)
        rev = msListRevenue(bundles, v, l)
        
        bid = targetPrice(bundles, rev, pp, True)
        numpy.testing.assert_array_equal(bid, [5,0], "Error: targetPrice test1 failed.")
        
if __name__ == "__main__":
    unittest.main()