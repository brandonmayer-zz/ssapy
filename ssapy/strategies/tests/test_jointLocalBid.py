import unittest
import numpy

from ssapy.strategies.jointLocalBid import jointLocalUpdate 
from ssapy import listBundles, msListRevenue

class test_jointLocalBid(unittest.TestCase):
    def setUp(self):
        self.samples2d = numpy.atleast_2d([[1,1],   [20,3], [10,7], [15,5],
                                           [10,30], [15,26],[17,33], [2,40],
                                           [30,30], [27,42],[30,38], [29,40],
                                           [42,20], [38,7], [40,15], [33,10]])
        
        self.bundles2d = listBundles(2)
        self.l2d = 1
        self.v2d = [20,10] 
        self.revenue2d = msListRevenue(self.bundles2d, self.v2d, self.l2d)
        
    def test_jointLocalUpdate(self):
        ibids = [25.,25.]
        print ibids
        targetBid = 0
        ibids[targetBid] = \
            jointLocalUpdate(self.bundles2d, self.revenue2d, 
                             ibids,targetBid, 
                             self.samples2d, True)
        
        print ibids

if __name__ == "__main__":
    unittest.main()