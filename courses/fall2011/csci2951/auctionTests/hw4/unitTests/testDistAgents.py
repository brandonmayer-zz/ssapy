from auctionSimulator.hw4.agents.straightMU import *
from auctionSimulator.hw4.agents.straightMU8 import *
from auctionSimulator.hw4.agents.targetMU import *
from auctionSimulator.hw4.agents.targetMU8 import *
from auctionSimulator.hw4.agents.targetMUS import *
from auctionSimulator.hw4.agents.targetMUS8 import *
from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.agents.riskAwareTP8 import *
from auctionSimulator.hw4.agents.riskAwareTMVS8 import *


import unittest
import numpy
import tempfile

class testDistAgents(unittest.TestCase):
    """
    Unit tests for agents who bid with distributions over price predictions.
    """

    def setUp(self):
        """
        Initialize some random distributions that will act as test data for 
        Self Confirming Price Predictions.
        """
        #make some fake data
        self.m = 5
        self.randomPriceVector = numpy.random.random_integers(1,10,self.m)
        
        self.mu = [5,3,2,1,1]
#        self.sigma = [10]*self.m
        self.sigma = numpy.random.random_integers(1,15,self.m)
        self.randomPriceDist = []
        self.randomPriceCount = []
        for good in xrange(self.m):
            randomPrices = numpy.random.normal(loc=self.mu[good],scale=self.sigma[good],size=10000)
            self.randomPriceDist.append(numpy.histogram(randomPrices,bins=range(0,51),density=True))
        #test a single distribution
        
    def test_straightMU(self):
        m = 5
        
        # test some of the pickle constructors for code coverage
        # similar to the point (straightMV) test case
        randomMargDist = margDistSCPP(self.randomPriceDist)
        
        tempFileObject = tempfile.NamedTemporaryFile('w+b', suffix='.pkl')
        
        randomMargDist.savePickle(tempFileObject.file)
        
        # set index to beggining of file to simulate close and re-open
        tempFileObject.file.seek(0)
        
        randomMargDist2 = margDistSCPP()
        
        randomMargDist2.loadPickle(tempFileObject.file)
        
        # test that the pickle methods work
        for idx in xrange(len(randomMargDist.data)):
            
            numpy.testing.assert_equal(randomMargDist.data[idx][0],
                                       randomMargDist2.data[idx][0], 
                                       err_msg = 'Pickling save/load failed')
        
            numpy.testing.assert_equal(randomMargDist.data[idx][1],
                                       randomMargDist2.data[idx][1], 
                                       err_msg = 'Pickling save/load failed')
        
        myStraightMU = straightMU(margDistPricePrediction = randomMargDist,name="myStraightMU")
        
        #make sure the data flows down super calls correctly
        self.assertEqual("myStraightMU",myStraightMU.name)
            
        print ''
        myStraightMU.printSummary()
        print''
        
        myStraightMU2 = straightMU(v=myStraightMU.v,l=myStraightMU.l)
        myStraightMU2.setPricePrediction(randomMargDist2)
        
        bid = myStraightMU.bid()
        
        bid2 = myStraightMU2.bid()
        
        numpy.testing.assert_equal(bid,bid2)
        
    def test_straightMU8(self):
        randomMargDist = margDistSCPP(self.randomPriceDist)
        
        myStraightMU8 = straightMU8(margDistPricePrediction = randomMargDist,name="myStraightMU8")
        
        print''
        
        myStraightMU8.printSummary()
        
    def test_targetMU(self):
        randomMargDist = margDistSCPP(self.randomPriceDist)
        
        myTargetMU = targetMU(margDistPricePrediction = randomMargDist,name="myTargetMU")
        
        print''
        
        myTargetMU.printSummary()
        
    def test_targetMU8(self):
        randomMargDist = margDistSCPP(self.randomPriceDist)
        
        myTargetMU8 = targetMU8(margDistPricePrediction = randomMargDist,name="myTargetMU8")
        
        print''
        
        myTargetMU8.printSummary()
        
    def test_targetMUS(self):
        randomMargDist = margDistSCPP(self.randomPriceDist)
        
        myTargetMUS = targetMUS(margDistPricePrediction = randomMargDist,name="myTargetMUS")
        
        print''
        
        myTargetMUS.printSummary()
        
    def test_targetMUS8(self):
        randomMargDist = margDistSCPP(self.randomPriceDist)
        
        myTargetMUS8 = targetMUS8(margDistPricePrediction = randomMargDist, name="myTargetMUS8")
        
        print''
        
        myTargetMUS8.printSummary()
        
    def test_riskAware(self):
        
        randomMargDist = margDistSCPP(self.randomPriceDist)
        
        myRiskAware = riskAware(m = self.m,
                                margDistPricePrediction = margDistSCPP(self.randomPriceDist),
                                A=10)
        
        myRiskAware.printSummary()
        
        print ''
        print 'Bid Test, myRiskAware.bid()'
        print myRiskAware.bid()
        print ''
        
    def test_riskAwareTP8(self):
        randomMargDist = margDistSCPP(self.randomPriceDist)
        
        myRiskAwareTP8 = riskAwareTP8(m = self.m,
                                      margDistPricePrediction = margDistSCPP(self.randomPriceDist),
                                      A                       = 10,
                                      name                    = "riskAwareTP8")
        
        print ''
        myRiskAwareTP8.printSummary()
        
        print ''
        print 'Bid test, myRiskAwareTP8.bid()'
        print myRiskAwareTP8.bid()
        print ''
        
    def test_riskAwareTMVS8(self):
        randomMargDist = margDistSCPP(self.randomPriceDist)
        
        print ''
        myRiskAwareTMVS8 = riskAwareTMVS8(m = self.m,
                                          margDistPricePrediction = margDistSCPP(self.randomPriceDist),
                                          A                       = 10,
                                          name                    = "riskAwareTMVS8") 
        
        print ''
        print myRiskAwareTMVS8.printSummary()
        print ''
        print 'Bid function test, myRiskAwareTMVS8.bid()'
        print myRiskAwareTMVS8.bid()
        print ''
        
        
        
if __name__ == "__main__":
    unittest.main()
    
    