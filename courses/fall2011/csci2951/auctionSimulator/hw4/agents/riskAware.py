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
    
    INPUTS:    
        m            := the total number of time slots up for auction
                
        l            := the target number of time slots for the specific agent
                        chosen at random from 0->m if not specified
                                
        v            := list of valuations for time slots. Must be of size m
                        chosen at random by same random proceedure
                        as Yoon & Wellman if not specified
                
        v_min        := the minimum valuation for a time slot
                
        v_max        := the maximum valuation for a time slot
        
        margDistPricePrediction := A price prediction to store on the object instance
    
        bidStrategy  := string, the name of the bidding strategy the riskAdverse
                        instance should use to bid once an optimal mupv bundle
                        has been found. Default = 'targetPrice'
        
        A            := Free parameter of the Mean Upper Variance Utility
                        Default = 1
                        
        name         := the name of this object instance
                        
    
    """
    def __init__(self,
                 m = 5,
                 v = None,
                 l = None,
                 vmin = 0,
                 vmax = 50,
                 margDistPricePrediction = None,
                 bidStrategy = "targetPrice",
                 A = 1,
                 name = "Anonymous",):
        #test input has correct type
        numpy.testing.assert_equal( isinstance(bidStrategy,basestring),
                                    True)
        
        #set the member variables
        self.bidStrategy = bidStrategy
        self.A = A
        
        #pass the remaining arguments upstream
        super(riskAware,self).__init__(m = m,
                                       v = v,
                                       l = l,
                                       vmin = vmin,
                                       vmax = vmax,
                                       margDistPricePrediction = margDistPricePrediction,
                                       name = name)
    
    @staticmethod        
    def type():
        return "riskAware"
    
    @staticmethod
    def upv(margDist = None):
        """
        Helper function to compute upper partial variance for each marginal distribution
        in margDist
        
        UPV = (E_F[price]-price)^2 if price > E_F[price]
                              0                 else
                              
        OUTPUTS:
            A 1d numpy.ndarray with size = number of bundles 
        """
        
        # use numpy.testing so that assert can't be turned off at compile time
        numpy.testing.assert_equal(isinstance(margDist,margDistSCPP), 
                                   True, 
                                   err_msg = 'Must provide an instance of margDistSCPP')
            
        expectedPrices = margDist.expectedPrices()
        
        upv = []
        for idx in xrange(expectedPrices.shape[0]):
            #get the bin edges
            binEdges = numpy.atleast_1d(margDist.data[idx][1])
            #the prices greater than the expected value
            upperPriceIndicies = numpy.nonzero(binEdges > expectedPrices[idx])[0]
            #take the last bin off b/c of the inclusion of the upper limit
            upperPrices = binEdges[upperPriceIndicies[:-1]]
            upperPriceProb = margDist.data[idx][0][upperPriceIndicies[:-1]]
            
            upperDiff = numpy.array( upperPriceProb*[d for d in itertools.imap( operator.sub,
                                                                                itertools.repeat(expectedPrices[idx], times=upperPrices.shape[0]),
                                                                                upperPrices ) ])
            
            #dot product will yeild sum of squares (variance)
#            upv.append( numpy.sum((upperDiff*upperDiff)*upperPriceProb, dtype=numpy.float) )
            upv.append( numpy.sum((upperDiff*upperDiff), dtype=numpy.float) ) 
                
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
        
        numpy.testing.assert_equal( isinstance(A,float) or isinstance(A,int),
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
        expectedSurplus = simYW.surplus(bundles, valuation, expectedPrices)
        
        #calculate the upper-partial variance over each marginal distribution
        margUpv = riskAware.upv(margDist=margDist)
        
        #make sure we have an upv for all goods listed in
        #the bundles
        numpy.testing.assert_equal(margUpv.shape[0],
                                   bundles.shape[1])
        
        #calculate the mupv utility for each good
        util = []
        for bundleIdx in xrange(bundles.shape[0]):
            util.append( expectedSurplus[bundleIdx] - .5*A*numpy.dot(margUpv,bundles[bundleIdx]) )
        
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
        
        numpy.testing.assert_equal( isinstance(A,float) or isinstance(A,int),
                                    True,
                                    err_msg='must specify a floating point value for A.' )
        
        numpy.testing.assert_equal( isinstance(margDist,margDistSCPP),
                                    True,
                                    err_msg='margDist must be an instance of margDistSCPP.' )
    
        #enumerate all bundles
        allBundles = riskAware.allBundles()
        
        #return the mean - upper paritial variance utilities for all bundles
        utility = riskAware.mUPV( bundles   = allBundles,
                                  valuation = valuation,
                                  l         = l,
                                  A         = A, 
                                  margDist  = margDist ) 
        
        
        expectedSurplus = riskAware.surplus(bundles, valuation, margDist.expectedPrices())
                                 
        
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
        numpy.testing.assert_equal( (bidStrategy == 'targetPrice'),
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
            expectedPrices = pricePrediction.expectedPrices()
            
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
        
    def bid(self,args={}):
        """
        Interface to bid
        
        Overides base margDistPredictionAgent.bid to to facilitate extra
        parameters that are needede to be passed to riskAware.SS()
        """
        bundles=self.allBundles(self.m)
        pricePrediction = None
        A = None
        bidStrategy = None
        
        if 'margDistPrediction' in args:
            if isinstance(args['margDistPrediction'], margDistSCPP):
                
                pricePrediction = args['margDistPrediction']
                
            elif isinstance(args['margDistPrediction'],list):
                
                pricePrediction = margDistSCPP(args['margDistPrediction'])
                
            else:
                print '----ERROR----'
                print 'pointPredictionAgent::bid'
                print 'unkown pointPricePrediction type'
                raise AssertionError
            
            
        else:
            assert isinstance(self.pricePrediction, margDistSCPP),\
                "Must specify a price prediction to bid."
            pricePrediction = self.pricePrediction
            
        if 'A' in args:
            A = args['A']
        else:
            A = self.A  
            
        if 'bidStrategy' in args:
            bidStrategy = args['bidStrategy']
        else:
            bidStrategy = self.bidStrategy
                
        return self.SS({'bundles':bundles,
                        'l':self.l,
                        'valuation':simYW.valuation(bundles, self.v, self.l),
                        'margDistPrediction':pricePrediction,
                        'bidStrategy':bidStrategy,
                        'A':A})
                
            
        
        

    def printSummary(self, args = {}):
        """
        Print a summary of agent state to standard out.
        """
        print "Agent Name              = {0}".format(self.name)
        print "Agent ID                = {0}".format(self.id)
        print "Agent Type              = {0}".format(self.type())
        print "Agent lambda            = {0}".format(self.l)
        print "Agent Valuation Vector  = {0}".format(self.v)
        print "Agent Risk Aversion (A) = {0}".format(self.A)
        
        assert 'margDistPricePrediction' in args or self.pricePrediction != None,\
            "Must specify a price prediction"
            
        if 'margDistPricePrediction' in args:
            
            assert isinstance(args['margDistPricePrediction'],margDistSCPP) or\
                isinstance(args['margDistPricePrediction'], tuple),\
                    "args['margDistPricePrediction'] must be a margDistSCPP or numpy.ndarray"
                    
            if isinstance(args['margDistPricePrediction'], margDistSCPP):
                
                pricePredicton = args['margDistPricePrediciton']
                
            elif isinstance(args['margDistPricePrediction'], tuple):
                
                pricePrediction = margDistSCPP(args['margDistPricePrediction'])
                
            else:
                print 'Should never get here'
                raise AssertionError
                
        else:
            pricePrediction = self.pricePrediction
            
        bundles = self.allBundles(self.m)
        
        valuation = self.valuation(bundles = bundles,
                                   v       = self.v,
                                   l       = self.l )
        
        mupv = self.mUPV( bundles   = bundles,
                          valuation = valuation,
                          l         = self.l,
                          A         = self.A,
                          margDist  = pricePrediction )
        
        expectedPriceVector = pricePrediction.expectedPrices()
        
        print 'Expected Price Vector = {0}'.format(expectedPriceVector)
        
        upv = self.upv(pricePrediction)
        
        print 'Marginal Upper Partial Variance = {0}'.format(upv)
        
        expectedSurplus = self.surplus(bundles     = bundles,
                                       valuation   = valuation,
                                       priceVector = expectedPriceVector)
        
        expectedCost = self.cost(bundles = bundles, 
                                 price   = expectedPriceVector)
        
        
        
        print 'Bundle | Valuation | Expected Cost | Expected Surplus | Upper Parial Variance | Mean Upper-Partial Variance Utility'
        
        for i in xrange(bundles.shape[0]):
                print "{0}  {1:^8} {2:^8.3} {3:^8.3} {4:^8.3} {5:^8.3}".format( bundles[i].astype(numpy.int),
                                                          valuation[i],
                                                          expectedCost[i],
                                                          expectedSurplus[i],
                                                          numpy.dot(upv,bundles[i]),
                                                          mupv[i])
         
        [optBundleAcq, optSurplusAcq]   = self.acq(priceVector = expectedPriceVector)
        
        [optBundleMupv, optSurplusMupv] = self.acqMUPV( bundles   = bundles,
                                                        valuation = valuation,
                                                        l         = self.l,
                                                        A         = self.A,
                                                        margDist  = pricePrediction)
        
        print 'Optimal Bundle ACQ:           {0}'.format(optBundleAcq.astype(numpy.int))
        print 'Optimal Expected Surplus ACQ: {0}'.format(optSurplusAcq)
        
        print 'Optimal Bundle MUPV:          {0}'.format(optBundleMupv.astype(numpy.int))
        print 'Optimal Surplus MUPV:         {0}'.format(optSurplusMupv)
        
        print 'Bidding Strategy:             {0}'.format(self.bidStrategy)
        print 'Bid = {0}'.format(self.bid())
        
        print ''
        