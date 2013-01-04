"""
This is auctionSimulator/hw4/agents/bidEvaluator.py

Author: Brandon A. Mayer
Date:   12/11/2011

Implementation of bidEvaluator as described in Yoon & Wellman 2011:

"Generate candidate bid vectors and evaluate them according to the given 
 price distribution. The BidEvaluator strategy uses other bidding
 strategies to propose candidates and estimates their performance
 by sampling from F and averaging over the resulting surpluses.
 
 For instance BidEvaluator(SMU8) generates candidates using
 straightMU8. Since each invocation of StraightMU8 employs a new
 draw of eight samples from F to estimate the (expected prices)
 we generally obtain different bids.
 
 We define BidEvaluator(SMU8) to generate four candidate bids using
 StrightMU8, which takes 32 samples from F. We employ another 32
 samples to evaluate these candidates for a total of 64 (samples)
 required by this strategy.
 
 The result of BidEvaluator(SMU8) is the candidate bid vector which 
 performed best on average according to the 32 test samples."


"""
from straightMU import *
from targetMUS import *
from riskAware import *

class bidEvaluatorBase(margDistPredictionAgent):
    @staticmethod
    def type():
        return "bidEvaluatorBase"
    
    @staticmethod
    def SS(**kwargs):
        raise AssertionError('Cannot bid with abstract bidEvaluatorBase')
    
    @staticmethod
    def checkArgs(**kwargs):
#        numpy.testing.assert_('m' in kwargs, 
#            msg="Must specify the number of goods to bid")
        
        numpy.testing.assert_('l' in kwargs,
            msg="Must specify the target number of goods (l).")
        
        numpy.testing.assert_('v' in kwargs,
            msg="Must specify the valuation vector of time slots (v).")
        
    @staticmethod
    def bid2bundle(bid = None, finalPrices = None):
        """
        Given a vector of bids and finalPrices, return the 
        bundle that was won.
        """
        numpy.testing.assert_(isinstance(bid,numpy.ndarray),
                              msg="bid must be an instance of numpy.ndarray")
        
        numpy.testing.assert_(isinstance(finalPrices,numpy.ndarray),
                              msg="finalPrices must be an instance of numpy.ndarray")
        
        numpy.testing.assert_equal(bid.shape,finalPrices.shape)
        
        return bid >= finalPrices
    
    @staticmethod
    def candidateAvgSurplus(**kwargs):
        """
        Given bid candidates, samples from the price distribution and the agents valuation vector
        v and target number of goods l, compute the average surplus realized by each candidate
        """
        try:
            candidates = kwargs['candidates']
        except KeyError:
            raise KeyError('Must specify the bid candidates, kwargs[\'candidates\'].')
        
        try:
            samples = kwargs['samples']
        except KeyError:
            raise KeyError('Must specify the samples with which to evaluate the candidates, kwargs[\'samples\'].')
        
        try:
            v = numpy.atleast_1d(kwargs['v'])
        except KeyError:
            raise KeyError('Must specify the agents valuation vector, v.')
        
        try:
            l = kwargs['l']
        except KeyError:
            raise KeyError('Must specify the target number of goods, kwargs[\'l\'].')            
            
        numpy.testing.assert_(l <= v.shape[0] and l > 0,
            msg = "l must be a positive integer <= v.shape[0]")
        
        numpy.testing.assert_equal(candidates.shape[1], v.shape[0], 
             err_msg="v must have one valuation per slot.")
        
        avgCandidateSurplus = numpy.zeros(candidates.shape[0])
        for i,candidate in enumerate(candidates):
            
            surplus = numpy.zeros(samples.shape[0])
            
            for j,sample in enumerate(samples):
                
                bundleWon = candidate > sample
                
                bundleValue = simYW.valuation(bundles = bundleWon,
                                              v       = v,
                                              l       = l)
                
                bundleCost = simYW.cost(bundleWon, candidates[i])
                
                surplus[j] = bundleValue - bundleCost
                
            avgCandidateSurplus[i] = numpy.mean(surplus, dtype = numpy.float)      
        
        return avgCandidateSurplus   
                            
    def bid(self, **kwargs):
        m                  = kwargs.get('m', self.m)
        v                  = kwargs.get('v', self.v)
        l                  = kwargs.get('l', self.l)
        margDistPrediction = kwargs.get('margDistPrediction', self.pricePrediction)
        bundles            = kwargs.get('bundles', self.allBundles(m))
        
        return self.SS(bundles            = bundles,
                       margDistPrediction = margDistPrediction,
                       m                  = m,
                       v                  = v,
                       l                  = l)
                       
        
        
        
class bidEvaluatorSMU8(bidEvaluatorBase):
    """
    BidEvaluator that generates 8 candidates via straightMU8 strategy and
    chooses the best that performs best (highest average surplus) w.r.t to
    32 samples from the price prediction distribution.
    """
    @staticmethod
    def type():
        return "bidEvaluatorSMU8"
    
    @staticmethod
    def SS(**kwargs):
        
        bidEvaluatorBase.checkArgs(**kwargs)
        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        m = kwargs.get('m', pricePrediction.m)
        
        bundles = kwargs.get('bundles',simYW.allBundles(m))      
        
        bidCandidates = kwargs.get('bidCandidates',[])
        
        if not bidCandidates:
            
            try:
                v = kwargs['v']
            except KeyError:
                raise KeyError('v is not in kwargs.')
            
            try:
                l = kwargs['l']
            except:
                raise KeyError('l is not in kwargs.')
            
            
            
            agent = straightMU8(margDistPricePrediction = pricePrediction,
                                m                       = m,
                                l                       = l,
                                v                       = v)
            
            bidCandidates = numpy.atleast_2d([agent.bid() for i in xrange(4)])

            
        else:
            bidCandidates = numpy.atleast_2d(bidCandidates)
            
        evalSamples = kwargs.get('evalSamples',pricePrediction.iTsample(nSamples = 32))
        
        avgCandidateSurplus = bidEvaluatorBase.candidateAvgSurplus(candidates = bidCandidates,
                                                                   samples    = evalSamples,
                                                                   v          = v,
                                                                   l          = l)
        
        #the bid is the candidate that has the highest
        #average surplus
        return bidCandidates[numpy.nonzero(avgCandidateSurplus == numpy.max(avgCandidateSurplus))[0][0]]
    
    
class bidEvaluatorSMU64(bidEvaluatorBase):
    """
    BidEvaluator that generates 8 candidates via straightMU8 strategy and
    chooses the best that performs best (highest average surplus) w.r.t to
    32 samples from the price prediction distribution.
    """
    @staticmethod
    def type():
        return "bidEvaluatorSMU8"
    
    @staticmethod
    def SS(**kwargs):
        
        bidEvaluatorBase.checkArgs(**kwargs)
        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        m = kwargs.get('m', pricePrediction.m)
        
        bundles = kwargs.get('bundles',simYW.allBundles(m))      
        
        bidCandidates = kwargs.get('bidCandidates',[])

        
        if not bidCandidates:
            
            
            
            
            
            agent = straightMU64(margDistPricePrediction = pricePrediction,
                                 m                       = m,
                                 l                       = l,
                                 v                       = v)
            
            bidCandidates = numpy.atleast_2d([agent.bid() for i in xrange(4)])

            
        else:
            bidCandidates = numpy.atleast_2d(bidCandidates)
            
        #4 candidates each draw 64 samples -> 4*64=256 samples
        evalSamples = kwargs.get('evalSamples',pricePrediction.iTsample(nSamples = 254))
        
        avgCandidateSurplus = bidEvaluatorBase.candidateAvgSurplus(candidates = bidCandidates,
                                                                   samples    = evalSamples,
                                                                   v          = v,
                                                                   l          = l)
        
        #the bid is the candidate that has the highest
        #average surplus
        return bidCandidates[numpy.nonzero(avgCandidateSurplus == numpy.max(avgCandidateSurplus))[0][0]]
    
class bidEvaluatorTMUS8(bidEvaluatorBase):
    """
    Bid evaluator using targetMUS8 as the underlying bid generator.
    """
    @staticmethod
    def type():
        return "BidEvaluatorTMUS8"
    
    
    @staticmethod
    def SS(**kwargs):
        
        try:
            v = kwargs['v']
        except KeyError:
            raise KeyError('Must specify v in kwargs')
            
        try:
            l = kwargs['l']
        except KeyError:
            raise KeyError('Must specify l in kwargs')
        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        m = kwargs.get('m',pricePrediction.m)
        
        bundles = kwargs.get('bundles', m)
        
        bidCandidates = kwargs.get('bidCandidates',[])
        
        if not bidCandidates:
            agent = targetMUS8( margDistPricePrediction = pricePrediction,
                                m                       = m,
                                l                       = l,
                                v                       = v)
            
            bidCandidates = numpy.atleast_2d([agent.bid() for i in xrange(4)])
            
        else:
            bidCandidates = numpy.atleast_2d(bidCandidates)
            
        evalSamples = kwargs.get('evalSamples',pricePrediction.iTsample(nSamples = 32))
                
        avgCandidateSurplus = bidEvaluatorBase.candidateAvgSurplus(candidates = bidCandidates,
                                                                   samples    = evalSamples,
                                                                   v          = v,
                                                                   l          = l)
        
        #the bid is the candidate that has the highest
        #average surplus
        return bidCandidates[numpy.nonzero(avgCandidateSurplus == numpy.max(avgCandidateSurplus))[0][0]]
    
class bidEvaluatorRaBase(bidEvaluatorBase):
    def __init__(self,**kwargs):
        self.A = kwargs.get('A',1)
        
        #pass upstream
        super(bidEvaluatorRaBase,self).__init__(**kwargs)
        
    @staticmethod
    def type():
        return "bidEvaluatorRaBase"
    
    def bid(self, **kwargs):
        
        margDistPrediction = kwargs.get('margDistPrediction', self.pricePrediction)
        m                  = kwargs.get('m', self.m)
        return self.SS(bundles            = kwargs.get('bundles', self.allBundles(m)),
                       margDistPrediction = margDistPrediction,
                       m                  = m,
                       v                  = kwargs.get('v', self.v),
                       l                  = kwargs.get('l', self.l),
                       A                  = kwargs.get('A', self.A) )
            
class bidEvaluatorRaTMUS8(bidEvaluatorRaBase):
    @staticmethod
    def type():
        return "bidEvaluatorRa8"
    
    @staticmethod
    def SS(**kwargs):
        try:
            v = kwargs['v']
        except KeyError:
            raise KeyError('v is not in kwargs.')
            
        try:
            l = kwargs['l']
        except:
            raise KeyError('l is not in kwargs.')
            
        try:
            A = kwargs['A']
        except:
            raise KeyError('A is not in kwargs')
        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        m = kwargs.get('m', pricePrediction.m)
        
        bundles = kwargs.get('bundles', simYW.allBundles(m))
        
        bidCandidates = kwargs.get('bidCandidates',[])
        
        nCandidates = kwargs.get('nCandidates',4)
        
        if not bidCandidates:
            agent = riskAwareTMUS8(margDistPricePrediction = pricePrediction,
                                   m                       = m,
                                   l                       = l,
                                   v                       = v,
                                   A                       = A)
            
            bidCandidates = numpy.atleast_2d([agent.bid() for i in xrange(nCandidates)])
            
        else:
            bidCandidates = numpy.atleast_2d(bidCandidates)
            
        evalSamples = kwargs.get('evalSamples',pricePrediction.iTsample(nSamples = 32))
            
        avgCandidateSurplus = bidEvaluatorBase.candidateAvgSurplus(candidates = bidCandidates,
                                                                   samples    = evalSamples,
                                                                   v          = v,
                                                                   l          = l)
        
        #the bid is the candidate that has the highest
        #average surplus
        return bidCandidates[numpy.nonzero(avgCandidateSurplus == numpy.max(avgCandidateSurplus))[0][0]]
        
