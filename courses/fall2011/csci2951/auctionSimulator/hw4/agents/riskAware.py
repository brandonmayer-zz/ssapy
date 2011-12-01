"""
this is /auctionSimulator/hw4/agents/riskAware.py

Author:    Brandon A. Mayer
Date:      11/23/2011
"""

from margDistPredictionAgent import *

class riskAware(margDistPredictionAgent):
    """
    Risk aware agent. This agent can adopt several strategies for bidding but
    chooses optimal bundle based on a modified mean variance utility function which
    is a more general case of the acquisition problem proposed by Boyan & Greenwald,2001
    and used in Yoon & Wellman 2011. The mean utility variance function is calculated 
    using upper partial variance instead of variance to account for the asymettric
    effect of price volitility on bundle acquisition
    """
    def __init__(self,
                 m = 5,
                 v = None,
                 l = None,
                 vmin = 0,
                 vmax = 50,
                 margDistPricePrediction = None,
                 name = "Anonymous",
                 bidStrategy = "targetPrice"):
        #test input has correct type
        numpy.testing.assert_equal( isinstance(bidStrategy,basestring),
                                    True)
        #set the variable
        self.bidStrategy = bidStrategy
        
        #pass the remaining arguments upstream
        super(riskAware,self).__init__(m = 5,
                                       v = None,
                                       l = None,
                                       vmin = 0,
                                       vmax = 50,
                                       margDistPricePrediction = None,
                                       name = "Anonymous")
    
    @staticmethod        
    def type(self):
        return "riskAware"
    
    @staticmethod
    def upv(margDist = None):
        """
        Helper function to compute upper partial variance for each marginal distribution
        in margDist
        
        UPV = (E_F[price]-price)^2 if price > E_F[price]
                              0                 else
        """
        
        # use numpy.testing so that assert can't be turned off at compile time
        numpy.testing.assert_equal(isinstance(margDist,margDistSCPP), 
                                   True, 
                                   err_msg = 'Must provide an instance of margDistSCPP')
            
        expectedPrices = margDist.expectedPrices()
        
        upv = []
        for idx in xrange(expectedPrices.shape[0]):
            #get the bin edges
            binEdges = numpy.atleast_1d(marginalPriceDistributions.data[idx][1])
    
            #the prices greater than the expected value
            upperPrices = binEdges[numpy.nonzero(binEdges > expectedValueVector[idx])]
            
            upperDiff = numpy.array( [d for d in itertools( operator.sub,
                                                            itertools.repeat(expectedPrices[goodIdx], times=upperPrices.shape[0]),
                                                            upperPrices ) ])
            
            #dot product will yeild sum of squares (variance)
            upv.append(numpy.dot(upperDiff,upperDiff))
                
        return numpy.atleast_1d(upv)
            
    @staticmethod
    def mUPV(bundles = None, valuation = None, l = None, A = None, margDist = None):
        """
        Yet another helper. This function enumerates utility over bundles but does not
        maximize.
        
        INPUTS:
            bundle                      :=  bit vector indicating which goods are in the bundle
                                            Can be a list of bundles or a single bundle
                                            
            valuation                   :=  a valuation for each element in bundle
            
            l                           :=  number of target time slots needed
            
            A                           := the risk adversion parameter       
            
            marginalPriceDistributions  :=  marginal probability distributions over
                                            the prices of goods in the bundle
        """
        #check for valid inputs
        numpy.testing.assert_equal( isinstance(bundles,numpy.ndarray),
                                    True,
                                    err_msg='bundles must be an instance of numpy.ndarray.' )
        
        numpy.testing.assert_equal( isinstance(valuation,numpy.ndarray),
                                    True,
                                    err_msg='valuation must be an instance of numpy.ndarray.' )
        
        numpy.testing.assert_equal( bundles.shape[0],
                                    valuation.shape[0] )
    
        numpy.testing.assert_equal( isinstance(l,int),
                                    True,
                                    err_msg='must specify an int l')
        
        numpy.testing.assert_equal( isinstance(A,float),
                                    True,
                                    err_msg='must specify a floating point value for A.' )
        
        numpy.testing.assert_equal( isinstance(margDist,margDistSCPP),
                                    True,
                                    err_msg='margDist must be an instance of margDistSCPP.' )
        
        #calculate the martinal expected prices
        expectedPrices = margDist.expectedPrices()
        
        #assert that we have an expected value for brice for ever
        #good in the enumerated bundles
        numpy.testing.assert_equal(expectedPrices.shape[0],
                                   bundles.shape[1])
        
        #given the expected marginal prices, calculated the expected surplus for each bundle
        expectedSurplus = self.surplus(bundles, valuation, expectedPrices)
        
        #calculate the upper-partial variance over each marginal distribution
        margUpv = upv(margDist=margDist)
        
        #make sure we have an upv for all goods listed in
        #the bundles
        numpy.testing.assert_equal(margUpv.shape[0],
                                   bundles.shape[1])
        
        #calculate the mupv utility for each good
        util = []
        for bundleIdx in xrange(bundles.shape[0]):
            util.append( expectedSurplust[bundleIdx] - .5*A*numpy.dot(margUpv,bundles[bundlIdx]) )
        
        return numpy.atleast_1d(util)
                                                                               
    @staticmethod
    def acqMUPV(bundles = None, valuation = None, l = None, A = None, margDist = None):
        """
        Compute optimal bundle using Mean Utility uper-partial variance
        function.
        We will maximize the utility:
        U = E_F[price] - .5*A*UPV
        
        UPV = (ExpectedSurplus-price)^2 if price > E_F[price]
                              0                 else
        
        A is a free parameter representing the agent's risk "adversness"
        A = 0 -> risk neutral (reduces to acq from Boyan & Greenwald)
        A < 0 -> gabmberl/risk lover, the agent gains utility from taking on
                 extra risk
        A > 0 -> risk adverse bidder, agent values safer bundles
        """
        #check for valid inputs
        numpy.testing.assert_equal( isinstance(bundles,numpy.ndarray),
                                    True,
                                    err_msg='bundles must be an instance of numpy.ndarray.' )
        
        numpy.testing.assert_equal( isinstance(valuation,numpy.ndarray),
                                    True,
                                    err_msg='valuation must be an instance of numpy.ndarray.' )
        
        numpy.testing.assert_equal( bundles.shape[0],
                                    valuation.shape[0] )
    
        numpy.testing.assert_equal( isinstance(l,int),
                                    True,
                                    err_msg='must specify an int l')
        
        numpy.testing.assert_equal( isinstance(A,float),
                                    True,
                                    err_msg='must specify a floating point value for A.' )
        
        numpy.testing.assert_equal( isinstance(margDist,margDistSCPP),
                                    True,
                                    err_msg='margDist must be an instance of margDistSCPP.' )
    
        #enumerate all bundles
        allBundles = self.allBundles()
        
        #return the mean - upper paritial variance utilities for each bundles
        utility = self.meanUpvUtil(allBundles, marginalPriceDistributions = marginalPriceDistributions, A = A)
        
        #pick the bundle that maximizes utility
        optBundleIdxList = numpy.nonzero(utility==numpy.max(utility))[0]
        
        optBundle = []
        optExpectedSurplus = []
        if len(optBundleIdxList) == 1:
            optBundle = allBundles[optBundleIdxList[0]]
            optExpectedSurplus = expectedSurplus[optBundleIdxList[0]]
        else: 
            #if we get here it means there are multiple bundles with the same maximal utility
            #pick the one that finishes first ("minimally maximal")
            t = float('inf')
            for idx in optBundleIdxList:
                tempBinList = allBundles[idx]
                cs = numpy.cumsum(tempBinList)
                tNew = (numpy.array(cs) >= self.l).nonzero()
                if tNew[0].any():
                    tNew = tNew[0][0]
                    if tNew < t:
                        optBundle = allBundles[idx]
                        optExpectedSurplus = expectedSurplus[idx]
                        
        return optBundle, optExpectedSurplus
                            

        
    @staticmethod
    def SS(args={}):
        """
        Default value of A if not spceified in args is 1
        
        Default bidding strategy if not specified is 'targetPrice'
        which bids the expected value of goods if the good is included
        in the optimal bundle under the mean upper-partial variance utility
        """
        
        #standard checks
        pricePrediction = margDistPredictionAgent.SS(args=args)
        
        #additional checks
        bidStrategy = None
        if 'bidStrategy' in args:
            bidStrategy = args['bidStrategy']
        else:
            bidStrategy = 'targetPrice'
            
        A = None
        if 'A' in args:
            A = args['A']
        else:
            A = 1
        
        #enumerate stratgies as they are implemented
        numpy.testing.assert_equal( ('bidStrategy' == 'targetPrice'),
                                    True,
                                    err_msg='Unknown bidding strategy')
            
#        optBundle, optExpectedSurplus = acqMeanUtilUPS(marginalPriceDistributions=args['distributionPricePrediction'],
#                                                       A = A)
        optBundle, optExpectedSurplus = riskAware.acqMUPV(bundles = args['bundles'], 
                                                          valuation = args['valuation'], 
                                                          l = args['l'], 
                                                          A = A, 
                                                          margDist = args['margDistPrediction'])
        
        if bidStrategy == 'targetPrice':
            #bid the expected values for the optimal bundle according to mean - upper partial variance function
            expectedPrices = pricePrediciton.expectedValues()
            
            bid = []
            for goodIdx in xrange(optBundle.shape[0]):
                if optBundle[goodIdx]:
                    bid.append(expectedPrices[goodIdx])
                else:
                    bid.append(0)
                    
            return bid
        else:
            #this shouldn't happen
            print 'Uknown bid strategy'
            raise AssertionError
