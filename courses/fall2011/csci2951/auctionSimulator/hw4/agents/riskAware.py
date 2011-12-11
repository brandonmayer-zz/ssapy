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
        upperPartialStd = kwargs['upperPartialVar']
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
    