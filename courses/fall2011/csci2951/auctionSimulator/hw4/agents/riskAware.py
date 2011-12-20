"""
this is /auctionSimulator/hw4/agents/riskAware.py

Author:    Brandon A. Mayer
Date:      11/23/2011
"""

from margDistPredictionAgent import *
from auctionSimulator.hw4.agents.targetPrice import *
from auctionSimulator.hw4.agents.targetMVS import *
from auctionSimulator.hw4.agents.targetMV import *
import copy

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
        
        name         := the name of this object instance
        
        ===================== riskAware Specific ========================
        A            := Free parameter of the Mean Upper Variance Utility
                        Default = 1
                        
    
    """
    def __init__(self, **kwargs):
        #set the member variables
        self.A = kwargs.get('A', 1)
        
        #pass the remaining arguments upstream
        super(riskAware,self).__init__(**kwargs)
    
    @staticmethod        
    def type():
        return "riskAware"
    

    @staticmethod
    def mupv(**kwargs):
        """
        Yet another helper. This function enumerates utility over bundles but does not
        maximize.
        
        INPUTS:
            bundle                      :=  bit vector indicating which goods are in the bundle
                                            Can be a list of bundles or a single bundle
            
            A                           := the risk adversion parameter       
            
            upperPartialVar             := the marginal upper partial standard deviations
                                           (an array with one value per good)
            
            expectedSurplus             := the expected surplus for each bundle
        """
        
        bundles         = kwargs['bundles']
        expectedSurplus = kwargs['expectedSurplus']
        upperPartialVar = kwargs['upperPartialVar']
        A               = kwargs['A']
        
        #check for valid inputs
        numpy.testing.assert_(isinstance(bundles,numpy.ndarray),
                              msg='bundles must be an instance of numpy.ndarray.')
        
        numpy.testing.assert_(isinstance(expectedSurplus, numpy.ndarray),
                              msg="expectedSurplus must be a numpy.ndarray")
                
        numpy.testing.assert_equal(bundles.shape[0],
                                    expectedSurplus.shape[0])
        
        numpy.testing.assert_( isinstance(upperPartialVar,numpy.ndarray),
                               msg="upv must be a numpy.ndarray")
        
        numpy.testing.assert_(upperPartialVar.shape[0] == bundles.shape[1],
                              msg="There must be one upper partial variance per good.")    
        
        numpy.testing.assert_(isinstance(A,float) or isinstance(A,int),
                              msg="A must be a float or int")
        
        util = []
        for bundleIdx in xrange(bundles.shape[0]):
            nGoods = numpy.sum(bundles[bundleIdx], dtype=numpy.float)
            
            if nGoods:
                util.append(expectedSurplus[bundleIdx] - A*float(1/nGoods)*numpy.dot(upperPartialVar,bundles[bundleIdx]) )
            else:
                #for the case where we don't bid on anything
                util.append(0)

        return numpy.atleast_1d(util)
    
    @staticmethod
    def mups(**kwargs):
        """
        Yet another helper. This function enumerates utility over bundles but does not
        maximize.
        
        Computes the average risk (average of upper partial std in the whole bundle)
        
        INPUTS:
            bundle                      :=  bit vector indicating which goods are in the bundle
                                            Can be a list of bundles or a single bundle
            
            A                           := the risk adversion parameter       
            
            upperPartialStd             := the marginal upper partial standard deviations
                                           (an array with one value per good)
            
            expectedSurplus             := the expected surplus for each bundle
        """
        
        bundles         = kwargs['bundles']
        expectedSurplus = kwargs['expectedSurplus']
        upperPartialStd = kwargs['upperPartialStd']
        A               = kwargs['A']
        
        #check for valid inputs
        numpy.testing.assert_(isinstance(bundles,numpy.ndarray),
                              msg='bundles must be an instance of numpy.ndarray.')
        
        numpy.testing.assert_(isinstance(expectedSurplus, numpy.ndarray),
                              msg="expectedSurplus must be a numpy.ndarray")
                
        numpy.testing.assert_equal(bundles.shape[0],
                                    expectedSurplus.shape[0])
        
        numpy.testing.assert_( isinstance(upperPartialStd,numpy.ndarray),
                               msg="upv must be a numpy.ndarray")
        
        numpy.testing.assert_(upperPartialStd.shape[0] == bundles.shape[1],
                              msg="There must be one upper partial variance per good.")    
        
        numpy.testing.assert_(isinstance(A,float) or isinstance(A,int),
                              msg="A must be a float or int")
        
        util = []
        for bundleIdx in xrange(bundles.shape[0]):
            nGoods = numpy.sum(bundles[bundleIdx],dtype=numpy.float)
            if nGoods:
                util.append( expectedSurplus[bundleIdx] - A*(1/nGoods)*numpy.dot(upperPartialStd,bundles[bundleIdx]) )
            else:
                #for the case where we don't bid on anything
                util.append(0)

        return numpy.atleast_1d(util)
        
                                          
    @staticmethod
    def acqMups(**kwargs):
        """
        Compute optimal bundle using Mean Utility upper-partial standard deviation
        
        Will maximize the utility"
        
        $U_i = E_F[price] - A*(1/\sum_(j=1)^m bundle_i)UPS$
        
        A is a free parameter representing the agent's risk "adversness"
        A = 0 -> risk neutral (reduces to acq from Boyan & Greenwald)
        A < 0 -> gabmberl/risk lover, the agent gains utility from taking on
                 extra risk
        A > 0 -> risk adverse bidder, agent values safer bundles
        """
        numpy.testing.assert_('A' in kwargs,
                              msg="Must specify A.")
        
        numpy.testing.assert_('bundles' in kwargs,
                              msg="Must enumerate possible bundles.")
        
        numpy.testing.assert_('l' in kwargs,
                              msg="Must specify l, the target number of goods")
        
        numpy.testing.assert_('expectedSurplus' in kwargs,
                              msg="Must enumerate expected surplus for each bundle")
        
        numpy.testing.assert_('upperPartialStd' in kwargs,
                              msg="Must specify an upper partial standard deviation for the distribution over each good.")
        
        bundles         = kwargs['bundles']
        l               = kwargs['l']
        expectedSurplus = kwargs['expectedSurplus']
        upperPartialStd = kwargs['upperPartialStd']
        A               = kwargs['A']
        
        #check for valid inputs  
        numpy.testing.assert_(isinstance(bundles,numpy.ndarray),
                              msg="bundles argument must be a numpy.ndarray")
        
        numpy.testing.assert_(isinstance(expectedSurplus,numpy.ndarray),
                              msg="expectedSurplus must be an numpy.ndarray")
        
        numpy.testing.assert_equal( bundles.shape[0],
                                    expectedSurplus.shape[0] )
    
        numpy.testing.assert_(isinstance(A,float) or isinstance(A,int),
                              msg='must specify a floating point value for A.' )
        
        numpy.testing.assert_(isinstance(upperPartialStd,numpy.ndarray),
                              msg="upperPartialStd must be a numpy.ndarray")
        
        numpy.testing.assert_equal(upperPartialStd.shape[0], bundles.shape[1],
                                   err_msg="There must be one upper partial standard deviation per bundle")
        
        utility = riskAware.mups( bundles         = bundles,
                                  expectedSurplus = expectedSurplus,
                                  upperPartialStd = upperPartialStd,
                                  A               = A)
        optBundleIdxList = numpy.nonzero(utility == numpy.max(utility))[0]
        
        optBundle, optExpectedUtility = simYW.minMaxBundle( bundles = bundles[optBundleIdxList], 
                                                            utility    = utility[optBundleIdxList],
                                                            l          = l)                                  
        return optBundle, optExpectedUtility                                 
        
                                                                               
    @staticmethod
    def acqMupv(**kwargs):
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
        bundles         = kwargs['bundles']
        l               = kwargs['l']
        expectedSurplus = kwargs['expectedSurplus']
        upperPartialVar = kwargs['upperPartialVar']
        A               = kwargs['A']
        
        #check for valid inputs  
        numpy.testing.assert_(isinstance(bundles,numpy.ndarray),
                              msg="bundles argument must be a numpy.ndarray")
        
        numpy.testing.assert_(isinstance(expectedSurplus,numpy.ndarray),
                              msg="expectedSurplus must be an numpy.ndarray")
        
        numpy.testing.assert_equal( bundles.shape[0],
                                    expectedSurplus.shape[0] )
    
        numpy.testing.assert_(isinstance(A,float) or isinstance(A,int),
                              msg='must specify a floating point value for A.' )
        
        numpy.testing.assert_(isinstance(upperPartialVar,numpy.ndarray),
                              msg="upperPartialVar must be a numpy.ndarray")
        
        numpy.testing.assert_equal(upperPartialVar.shape[0], bundles.shape[1],
                                   err_msg="There must be one upper partial variance per bundle")
        
        utility = riskAware.mupv(bundles         = bundles, 
                                 expectedSurplus = expectedSurplus, 
                                 upperPartialVar = upperPartialVar, 
                                 A               = A)

        
        #pick the bundle that maximizes utility
        optBundleIdxList = numpy.nonzero(utility==numpy.max(utility))[0]
        
        
        optBundle, optExpectedUtility = simYW.minMaxBundle( bundles[optBundleIdxList], 
                                                            utility[optBundleIdxList])
                             
        return numpy.array(optBundle,dtype=bool), optExpectedUtility
                    
        
    @staticmethod
    def SS(**kwargs):
        """
        Default value of A if not spceified is 1
        
        Default bidding strategy if not specified is 'targetPrice'
        which bids the expected value of goods if the good is included
        in the optimal bundle under the mean upper-partial variance utility
        """
        
        #standard checks
        numpy.testing.assert_('A' in kwargs,
                              msg="Must specify A parameter.")
        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)    
        
        expectedPrices = kwargs.get('expectedPrices',pricePrediction.expectedPrices())
        
        upperPartialStd = pricePrediction.margUps(expectedPrices = expectedPrices)
                    
        expectedSurplus = riskAware.surplus(kwargs['bundles'],
                                            kwargs['valuation'],
                                            expectedPrices)
        
        optBundle, optMups = riskAware.acqMups(bundles         = kwargs['bundles'],
                                               expectedSurplus = expectedSurplus,
                                               upperPartialStd = upperPartialStd,
                                               l               = kwargs['l'],
                                               A               = kwargs['A'])
        
        return targetPrice.bundleBid(pointPricePrediction = expectedPrices,
                                     bundle               = optBundle)
                
        
    def bid(self,**kwargs):
        """
        Interface to bid
        
        Overides base margDistPredictionAgent.bid to to facilitate extra
        parameters that are needede to be passed to riskAware.SS()
        """      
        
        return self.SS(bundles            = self.allBundles(self.m),
                       margDistPrediction = self.pricePrediction,
                       A                  = self.A,
                       valuation          = self.valuation(self.allBundles(self.m),self.v,self.l),
                       l                  = self.l)
            
    def printSummary(self,**kwargs):
        """
        Print a summary of agent state to standard out.
        """
        print "Agent Name              = {0}".format(self.name)
        print "Agent ID                = {0}".format(self.id)
        print "Agent Type              = {0}".format(self.type())
        print "Agent lambda            = {0}".format(self.l)
        print "Agent Valuation Vector  = {0}".format(self.v)
        print "Agent Risk Aversion (A) = {0}".format(self.A)
        
        pricePrediction = self.pricePrediction
            
        bundles = self.allBundles(self.m)
        
        valuation = self.valuation(bundles = bundles,
                                   v       = self.v,
                                   l       = self.l )
        
        expectedPrices = kwargs.get('expectedPrices', pricePrediction.expectedPrices())

        expectedSurplus = self.surplus(bundles, valuation, expectedPrices)
        
        expectedCost = self.cost(bundles = bundles, 
                                 price   = expectedPrices)
        
        upperPartialStd = pricePrediction.margUps(expectedPrices = expectedPrices)
       
        mups = self.mups(bundles         =   bundles, 
                         expectedSurplus = expectedSurplus, 
                         upperPartialStd = upperPartialStd, 
                         A               = self.A)
        
        print 'Expected Price Vector = {0}'.format(expectedPrices)
        
        print 'Marginal Upper Partial Standard Deviation = {0}'.format(upperPartialStd)
        
        table = [ ['Bundle', 'Valuation', 'Expected Cost', 'Expected Surplus', 'Bundle Average Risk', 'MUPS Utility'] ]
        
        
        for i in xrange(bundles.shape[0]):
            avgRisk = 0.0
            if numpy.sum(bundles[i]):
                avgRisk = (1/numpy.sum(bundles[i],dtype=numpy.float))*numpy.dot(upperPartialStd,bundles[i])
            else:
                avgRisk = 0.0
                
            table.append([ str(bundles[i].astype(numpy.int)), "{0:.5}".format(float(valuation[i])), 
                           "{0:.5f}".format(float(expectedCost[i])), "{0:.5f}".format(float(expectedSurplus[i])),\
                           "{0:.5f}".format(float(avgRisk)), "{0:.5f}".format(float(mups[i])) ]) 
                          
                
        
        ppt(sys.stdout,table)
        
        [optBundleAcq, optSurplusAcq]   = self.acq(priceVector = expectedPrices)
        
        [optBundleMupv, optMups] = self.acqMups( bundles              = bundles,
                                                 expectedSurplus      = expectedSurplus,
                                                 upperPartialStd      = upperPartialStd,
                                                 A                    = self.A,
                                                 l                    = self.l)
        
        print ''
        print ''
        
        print 'Optimal Bundle ACQ:           {0}'.format(optBundleAcq.astype(numpy.int))
        print 'Optimal Expected Surplus ACQ: {0}'.format(optSurplusAcq)
        
        print 'Optimal Bundle mups:          {0}'.format(optBundleMupv.astype(numpy.int))
        print 'Optimal mups:                 {0}'.format(optMups)
        
        print 'Bid = {0}'.format(self.bid())
        
        print ''
        
       
class riskAwareTP8(riskAware):
    @staticmethod
    def type():
        return "riskAwareTP8"
    
    @staticmethod
    def SS(**kwargs):
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        tkwargs = copy.deepcopy(kwargs)
        
        tkwargs['expectedPrices'] = pricePrediction.expectedPrices(method   = 'iTsample',
                                                                   nSamples = 8)
        
        return riskAware.SS(**tkwargs)
        
    def printSummary(self,**kwargs):
        
        tkwargs = copy.deepcopy(kwargs)
        
        tkwargs['expectedPrices'] = kwargs.get('expectedPrices', 
                                               self.pricePrediction.\
                                               expectedPrices(method   = 'iTsample',
                                                              nSamples = 8))
        
        super(riskAwareTP8,self).printSummary(**tkwargs)
        
class riskAwareTP64(riskAware):
    @staticmethod
    def type():
        return "riskAwareTP64"
    
    @staticmethod
    def SS(**kwargs):
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        tkwargs = copy.deepcopy(kwargs)
        
        tkwargs['expectedPrices'] = pricePrediction.expectedPrices(method   = 'iTsample',
                                                                   nSamples = 64)
        
        return riskAware.SS(**tkwargs)
        
    def printSummary(self,**kwargs):
        
        tkwargs = copy.deepcopy(kwargs)
        
        tkwargs['expectedPrices'] = kwargs.get('expectedPrices', 
                                               self.pricePrediction.\
                                               expectedPrices(method   = 'iTsample',
                                                              nSamples = 64))
        
        super(riskAwareTP64,self).printSummary(**tkwargs)
        
class riskAwareTP256(riskAware):
    @staticmethod
    def type():
        return "riskAwareTP256"
    
    @staticmethod
    def SS(**kwargs):
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        tkwargs = copy.deepcopy(kwargs)
        
        tkwargs['expectedPrices'] = pricePrediction.expectedPrices(method   = 'iTsample',
                                                                   nSamples = 256)
        
        return riskAware.SS(**tkwargs)
        
    def printSummary(self,**kwargs):
        
        tkwargs = copy.deepcopy(kwargs)
        
        tkwargs['expectedPrices'] = kwargs.get('expectedPrices', 
                                               self.pricePrediction.\
                                               expectedPrices(method   = 'iTsample',
                                                              nSamples = 256))
        
        super(riskAwareTP256,self).printSummary(**tkwargs)
        
    
    
        
class riskAwareTMUS(riskAware):
    @staticmethod
    def type():
        return "riskAwareTMUS"
    
    @staticmethod
    def SS(**kwargs):
        
        numpy.testing.assert_('A' in kwargs,
                              msg="Must specify A parameter.")
        
        numpy.testing.assert_('l' in kwargs,
                              msg="Must specify l, the target number of goods.")
        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        bundles = kwargs.get('bundles', simYW.allBundles(pricePrediction.m))
        
        expectedPrices = kwargs.get( 'expectedPrices', 
                pricePrediction.expectedPrices() )
        
        expectedSurplus = kwargs.get('expectedSurplus',
                riskAware.surplus(bundles, kwargs['valuation'], expectedPrices))
        
        upperPartialStd = kwargs.get('upperPartialStd',
                pricePrediction.margUps(expectedPrices = expectedPrices))
        
        optBundle, optups = riskAware.acqMups( bundles         = bundles, 
                                               l               = kwargs['l'],
                                               A               = kwargs['A'],
                                               upperPartialStd = upperPartialStd, 
                                               expectedSurplus = expectedSurplus )
        
        return targetMVS.bundleBid(bundle               = optBundle,
                                   pointPricePrediction = expectedPrices,
                                   valuation            = kwargs['valuation'],
                                   l                    = kwargs['l'])
                                                                                     
        
        
class riskAwareTMUS8(riskAware):
    @staticmethod
    def type():
        return "riskAwareTMUS8"
    
    @staticmethod
    def SS(**kwargs):
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        #so as not to mutate the original arguments
        tkwargs = copy.deepcopy(kwargs)
        
        tkwargs['expectedPrices'] = pricePrediction.expectedPrices(method   = 'iTsample', 
                                                                   nSamples = 8)
        
        return riskAwareTMUS.SS(**tkwargs)
                                                                    
        
    def printSummary(self,**kwargs):
        """
        Print a summary of agent state to standard out.
        """
        tkwargs = copy.deepcopy(kwargs)
        
        tkwargs['expectedPrices'] = kwargs.get('expectedPrices', 
                                               self.pricePrediction.\
                                               expectedPrices(method   ='iTsample', nSamples = 8))
                                                                        
        super(riskAwareTMUS8,self).printSummary(**tkwargs)
        
        
class riskAwareTMUS64(riskAware):
    @staticmethod
    def type():
        return "riskAwareTMUS64"
    
    @staticmethod
    def SS(**kwargs):
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        tkwargs = copy.deepcopy(kwargs)
        
        tkwargs['expectedPrices'] = pricePrediction.expectedPrices(method   = 'iTsample',
                                                                   nSamples = 64)
        
        return riskAwareTMUS.SS(**tkwargs)
        
    def printSummary(self,**kwargs):
        """
        Print a summary of agent state to standard out.
        """
        tkwargs = copy.deepcopy(kwargs)
        
        tkwargs['expectedPrices'] = kwargs.get('expectedPrices', 
                                               self.pricePrediction.\
                                               expectedPrices(method   ='iTsample', 
                                                              nSamples = 64))
                                                                        
        super(riskAwareTMUS64,self).printSummary(**tkwargs)  
        
class riskAwareTMUS256(riskAware):
    @staticmethod
    def type():
        return "riskAwareTMUS256"
    
    @staticmethod
    def SS(**kwargs):
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        tkwargs = copy.deepcopy(kwargs)
        
        tkwargs['expectedPrices'] = pricePrediction.expectedPrices(method   = 'iTsample',
                                                                   nSamples = 256)
        return riskAwareTMUS.SS(**tkwargs)
    
    def printSummary(self,**kwargs):
        """
        Print a summary of agent state to standard out.
        """
        tkwargs = copy.deepcopy(kwargs)
        
        tkwargs['expectedPrices'] = kwargs.get('expectedPrices', 
                                               self.pricePrediction.\
                                               expectedPrices(method   ='iTsample', 
                                                              nSamples = 256))
                                                                        
        super(riskAwareTMUS256,self).printSummary(**tkwargs)  
        
class riskAware2(riskAware):
    @staticmethod
    def type():
        return 'riskAware2'
    
    @staticmethod
    def _bidCost(**kwargs):
        """
        Return the expected cost of bundle.
        
        Parameters
        ----------
        bids: numpy.ndarray
            The array of bids on each good
            
        bidProb: numpy.ndarray
            The probability that each bid in the bids array
            is the closing price
            
        Returns
        -------
        expectedCost: scalar
            numpy.dot(bids,bidProb)
        """
        try:
            bidProb = numpy.atleast_1d(kwargs['bidProb'])
        except:
            raise KeyError('Must specify bidProb')
        
        try:
            bids = numpy.atleast_1d(kwargs['bids'])
        except:
            raise KeyError('Must specify the bids')
        
        return numpy.dot(bidProb,bids)
    
    def bidCost(self,**kwargs):
        """
        Calculate the expected cost given a vector of bids
        
        Parameters
        ----------
        bids: numpy.ndarray
            The array of bids for each good
        """
        bids = numpy.atleast1d( kwargs.get('bids') )
        
        if not bids:
            raise AssertionError('Must specify bids.')
        
        numpy.testing.assert_equal(bids.shape[0], self.m, 
            err_msg='Must specify a bid for each good.')
        
        bidProb = self.pricePrediction.bidPdf(bids)
        
        return self._bidCost(bids = bids, bidProb = bidProb)
    
    @staticmethod
    def _bidBundle(**kwargs):
        """
        Calcualte the probability that a given bundle will be
        the bundle that is won given a probability of winning the goods
        given our bids
        
        We are assuming that the goods contained in a bundle are independent
        thus the probability of winning a bundle is the product of the 
        probability of winning the goods in the bundle times the probability
        of losing the goods that are not in the bundle.
        
        Parameters
        ----------
        bidProb: numpy.ndarray dtype = float
            An array in which each element contains the probability that
            a bid will be the closing price of the auction Pr[closing price = bid]
            
        bundle: numpy.ndarray dtype = bool
            A target bundle. A bit vector representing the goods won at 
            auction
            
        Return
        ------
        finalBundleProb: scalar
            Pr[bundle = FinalBundle]
        """
        try:
            bidProb = numpy.atleast_1d(kwargs['bidProb'])
        except:
            raise KeyError('Must specify bidProb.')
        try:
            bundle = numpy.atleast_1d(kwargs['bundle'])
        except:
            raise KeyError('Must specify target Bundle.')
        
        numpy.testing.assert_equal(bidProb.shape, bundle.shape, 
            err_msg="bidProb and bundle must have the same shape.")
        
        #use nat. log to protect against underflow
        #note le pun
        winSum  = 0.0
        loseSum = 0.0
        for i, good in enumerate(bundle):
            if good:
                if bidProb[i] < numpy.finfo(float).eps:
                    winSum += numpy.log(numpy.finfo(float).eps)
                else:
                    winSum += numpy.log(bidProb[i])
            else:
                if bidProb[i] < numpy.finfo(float).eps:
                    loseSum += numpy.log(numpy.finfo(float).eps)
                else:
                    loseSum += numpy.log(bidProb[i])
                
                
            
        return numpy.exp(winSum+loseSum)
                
    @staticmethod
    def _bidValuation(**kwargs):
        """
        Calculate the expected valuation given a bid.
        
        We don't need to consider the bid explicitly in this function
        only the probability of winning each good given a bid vector
        therefore the parameter of interest is bidProb which is the marginal
        probability of winning each good given whatever the bid was.
        
        Parameters
        ----------
        bidProb: numpy.ndarray dtype = float
            An array (or list) in which each element contains the probability that
            a bid will be the closing price of the auction, Pr[closing price = bid]
            
        bundles: numpy.ndarray dtype = float (2 dimensional)
            A numpy.ndarray or 2d list which enumerate the valid bundles
            
        valuation: numpy.ndarray (1 dimensional)
            A numpy.ndarray or list which enumerates the valuations 
            for a given bundle.
            
        Return
        ------
        expectedValuation: scalar
            sum for all bundles valuation*Pr(X_i = X_final)
            
        """
        try:
            valuation = numpy.atleast_1d(kwargs['valuation'])
        except:
            raise KeyError('Must provide a vector of valuations over bundles.')
        
        try:
            bundles = numpy.atleast_2d(kwargs['bundles'])
        except:
            raise KeyError('Must provide a single or list of bundles.')
        
        try:
            bidProb = numpy.atleast_1d(kwargs['bidProb'])
        except:
            raise KeyError('Must specify bidProb.')
        
        numpy.testing.assert_equal(bundles.shape[0], valuation.shape[0], 
            err_msg = "Must provide a single valuation for each bundle.")
        
        numpy.testing.assert_equal(bundles.shape[1], bidProb.shape[0],
            err_msg = "Must have a probability for winning each possible good in a bundle.")
        
        expectedValuation = 0.0
        for i, bundle in enumerate(bundles):
            probFinalBundle = riskAware2._bidBundle(bundle  = bundle,
                                                    bidProb = bidProb)
            expectedValuation += valuation[i]*probFinalBundle
        
        return expectedValuation
    
    def bidValuation(self,**kwargs):
        bundles   = kwargs.get('bundles',self.allBundles(self.m))
        
        v = kwargs.get('v', self.v)
        
        l = kwargs.get('l', self.l)
        
        valuation = kwargs.get('valuation', self.valuation(bundles,v,l))
        
        bidProb = numpy.atleast_1d(kwargs.get('bidProb'))
        
        if bidProb.shape == 0:
            try:
                bids = kwargs['bids']
            except:
                raise AssertionError('Must specify bidProb or bids.')
            
            margDist = kwargs.get('margDistPrediction', self.pricePrediction)
            
            bidProb = margDist.bidPdf(bids = bids, kind = 'cubic')
            
        
        return self._bidValuation(bundles = bundles,
                                  bidProb = bidProb,
                                  valuation = valuation)
        
    def bidSurplus(self,**kwargs):
        try:
            bids = numpy.atleast_1d(kwargs['bids'])
        except:
            raise KeyError('Must specify bid to calculate resulting expected surplus')
            
        bundles    = kwargs.get('bundles',self.allBundles(self.m))
        v          = kwargs.get('v', self.v)
        l          = kwargs.get('l', self.l)
        valuation  = kwargs.get('valuation',self.valuation(bundles, v, l))    
        
        bidProb = numpy.atleast_1d(kwargs.get('bidProb'))
        
        if bidProb == None:
            
            
            margDist   = kwargs.get('margDistPrediction', self.pricePrediction)
            interpKind = kwargs.get('interpKind', 'linear')
            bidProb = margDist.bidPdf(bids = bids,
                                      kind = interpKind)
            
        bidVal = self.bidValuation(bundles = bundles,
                                   valuation = valuation,
                                   bidProb = bidProb)
        
        bCost = self._bidCost(bidProb = bidProb,
                              bids = bids)
        
        return bidVal - bCost
        
    def bidRisk(self, **kwargs):
        """
        Calculate the risk incurred given either a bid or the probability of
        winning marginal goods given the bid.
        
        Parameters
        ----------
        One of the two must be specified, bidProb or bids
        bidProb: numpy.ndarray (1 dimensional)
            The elements of bidProb are the marginal probabilities of 
            winning the i'th good given a particular bid.
            
        bids: numpy.ndarray (1 dimensional)
            The 
        """
        
        A        = kwargs.get('A', self.A)        
        bidProb  = kwargs.get('bidProb')
        margDist = kwargs.get('margDistPrediction', self.pricePrediction)
        
        if bidProb.shape[0] == 0:
            try:
                bids = kwargs['bids']
            except:
                raise AssertionError('Must specify bids for goods.')
            
            
        
            interpKind = kwargs.get('interpKind', 'linear')
        
            bidProb  = margDist.bidPdf(bids = bids,
                                       kind = interpKind)
        
        ups = kwargs.get('ups',margDist.margUps())
        
        return A*numpy.dot(ups,bidProb)
               
    def bidUtility(self, **kwargs):
        try:
            bids = numpy.atleast_2d(kwargs['bids'])
        except:
            raise KeyError('Must specify potential bid to calculate utility.')
        
        bundles   = numpy.atleast_2d(kwargs.get('bundles', self.allBundles(self.m)))
        v         = kwargs.get('v', self.v)
        l         = kwargs.get('l', self.l)
        valuation = numpy.atleast_1d(kwargs.get('valuation',self.valuation(bundles,v,l)))
        margDist  = kwargs.get('margDistPrediction', self.pricePrediction)
        A         = kwargs.get('A', self.A)
        
        numpy.testing.assert_equal(bundles.shape[0], valuation.shape[0],
            err_msg="Must specify one valuation for each bundle.")
                
        # precompute the bid prob so its not done again and again
        # in the helper functions
        utility = numpy.zeros(bids.shape[0])
        for i in xrange(bids.shape[0]):
            bidProb = margDist.bidPdf(bids=bids[i])
                    
            bSurplus = self.bidSurplus(bids               = bids[i],
                                       bidProb            = bidProb,
                                       bundles            = bundles,
                                       valuation          = valuation)
                                       
            
            bRisk = self.bidRisk(bidProb = bidProb,
                                 A    = A)
            
            utility[i] = bSurplus - bRisk
            
        return utility
    
class riskEvaluator8(riskAware2):
    @staticmethod
    def type():
        return "riskEvaluator8"
    
    def bid(self,**kwargs):
        margDist = kwargs.get('margDistPrediction', self.pricePrediction)
        
        samples = kwargs.get('samples', margDist.iTsample(nSamples = 8))
        
        utility = self.bidUtility(bids=samples)
        
        maxIdx = numpy.nonzero(utility==numpy.max(utility))[0]
        
        if maxIdx.shape[0] > 1:
            #randomly pick
            maxIdx = numpy.random.shuffle(maxIdx)
            
        return samples[maxIdx[0]]
    
class riskEvaluator64(riskAware2):
    @staticmethod
    def type():
        return "riskEvaluator64"
    
    def bid(self,**kwargs):
        
        margDist = kwargs.get('margDistPrediction', self.pricePrediction)
        
        samples = kwargs.get('samples', margDist.iTsample(nSamples = 64))
        
        utility = self.bidUtility(bids=samples)
        
        maxIdx = numpy.nonzero(utility==numpy.max(utility))[0]
        
        if maxIdx.shape[0] > 1:
            #randomly pick
            maxIdx = numpy.random.shuffle(maxIdx)
            
        return samples[maxIdx[0]]
    
class riskEvaluator256(riskAware2):
    @staticmethod
    def type():
        return "riskEvaluator256"
    
    def bid(self,**kwargs):
        margDist = kwargs.get('margDistPrediction', self.pricePrediction)
        
        samples = kwargs.get('samples', margDist.iTsample(nSamples = 256))
        
        utility = self.bidUtility(bids=samples)
        
        maxIdx = numpy.nonzero(utility == numpy.max(utility))[0]
        
        if maxIdx.shape[0] > 1:
            #randomly pick
            maxIdx = numpy.random.shuffle(maxIdx)
            
        return samples[maxIdx[0]]
    
        
        
        
        
        
        