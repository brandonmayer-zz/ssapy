#from auctionSimulator.hw4.agents.straightMU import *
#from auctionSimulator.hw4.agents.targetMU import *
#from auctionSimulator.hw4.agents.targetMUS import *
#from auctionSimulator.hw4.agents.averageMU import *
#from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.agents.targetMU import *
from auctionSimulator.hw4.agents.straightMU import *


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
        self.sigma = [.2]*self.m
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
        
  
        
if __name__ == "__main__":
    unittest.main()