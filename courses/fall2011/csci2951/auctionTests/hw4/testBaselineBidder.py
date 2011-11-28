"""
this is /auctionTests/testBaselineBidder.py

Author:    Brandon A. Mayer
Date:      11/27/2011

Test baselineBidder agent
"""
from auctionSimulator.hw4.agents.baselineBidder import *

import numpy
import unittest

class testBaselineBidder(unittest.TestCase):
    """
    Unit test worker class for baselineBidder.
    """
    def test_baselineBidderBasics(self):
        """
        Test the general framework of the baselineBidder
        """
        m = 5
        
        name = "myBaselineBidder"
        myBaselineBidder = baselineBidder(m=5,name=name)
        
        #check the name is passed down the constructors correctly
        self.assertEqual(name,myBaselineBidder.name)
        
        self.assertEqual(m, myBaselineBidder.m)
        
        #some more of that ocular method
        myBaselineBidder.printSummary()
        

if __name__ == "__main__":
    unittest.main()