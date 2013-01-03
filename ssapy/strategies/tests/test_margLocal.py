import os
import pickle
import unittest

from ssapy import listBundles, msListRevenue, msRandomValueVector
from ssapy.strategies.margLocalBid import margLocalBid


class test_margLocalBid(unittest.TestCase):
    def setUp(self):
        self.ppFile = os.path.realpath("./jointGmmScppHob_straightMU8_m5_n8_00013.pkl")
        with open(self.ppFile,'r') as f:
            self.pp = pickle.load(f)
        
    def test_vanillia(self):
        m = 5
        bundles = listBundles(m)
        v,l = msRandomValueVector(0, 50, m)
        revenue = msListRevenue(bundles, v, l)
        
        print margLocalBid(bundles = bundles, valuation = revenue, pricePrediction = self.pp, verbose = True)
        
        
if __name__ == "__main__":
    unittest.main()
        
        