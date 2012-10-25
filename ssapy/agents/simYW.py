"""
This is /auctionSimulator/hw4/agents/simYW.py

Author:    Brandon A. Mayer
Date:      11/26/2011

A base class for agents who participate in simultaneous auctions of the type
described by Yoon & Wellman 2011
"""
from agentBase import *
import itertools
import numpy
import operator

class simYW(agentBase):
    """
    Base class for agents competing in the auction for time slots described by
    Yoon & Wellman 2011.
    
    Note: 
        I made the functions:
        
                        allBundles(nGoods = 5)
                        valuation(bundles = None, v = None, l= None)
                        cost(bundles = None, price = None)
                        surplus(bundles=None, valuation = None, priceVector = None,)
                        bundleFromIndex(index=None, nGoods = 5)
                        acqYW(bundles = None, valuation = None, l = None, priceVector = None)
                        
        static functions on purpose to keep the class light. I wanted the
        class to store the data specific to the Yoon & Wellman specification as
        well as have the functions necessary to manipulate these data but I didn't
        feel these funcitons should be attached to every class instance. This also
        offers the added ability to specify the parameters of these functions rather
        than compute for class specific instances.
    """
    
    def __init__(self, **kwargs):
        """
            INPUTS:
                m            := the total number of time slots up for auction
                
                l            := the target number of time slots for the specific agent
                                chosen at random from 0->m if not specified
                                
                v            := list of valuations for time slots. Must be of size m
                                chosen at random by same random proceedure
                                as Yoon & Wellman if not specified
                
                v_min        := the minimum valuation for a time slot
                
                v_max        := the maximum valuation for a time slot
                
            NOTES:
                Though I do not store an explicit array of possible bundles
                to save space, we can imagine that there exists a list of bundles, each
                is a binary vector where a 1 in the t^th position indicates that the
                t^th good is included in the bundle. 
                
                If we were to enumerate all bundles, we could count from 0->(self.l-1) 
                e.g. self.l = 3 implies a list of
                [0, 0, 0]
                [0, 0, 1]
                ...
                [1, 1, 1]
                
                I assume big Endianness, that is the msb of the binary representation indicates
                slot one the lsb is then the (self.m - 1)^st good
                
                e.g. [1,0,0] is a bundle containing the first slot and has an index into our "virtual"
                bundle list of 4.
                
                If we want to convert an index into a bundle, just convert the index to binary
                and create the appropriately sized list, padding with zeros as necessary and 
                dictated by self.m
        """    
        self.m = kwargs.get('m',5)
        
        self.l = kwargs.get('l',numpy.random.random_integers(low = 1, high = self.m))     
        
        self.vmin = kwargs.get('vmin',0)
            
        self.vmax = kwargs.get('vmax',50)   
        
        if 'v' in kwargs:    
            self.v = numpy.atleast_1d(kwargs['v'])
            numpy.testing.assert_equal(self.v.shape[0], self.m,
                                       err_msg="self.v.shape[0] = {0} != self.m = {1}".format(self.v.shape[0],self.m))
        else:
            self.v = self.randomValueVector(vmin = self.vmin, 
                                            vmax = self.vmax, 
                                            m    = self.m,
                                            l    = self.l)[0]
            
        # a bit vector indicating which items where won
        # at auction
        self.bundleWon = kwargs.get('bundleWon')
        
        # a vector of final prices for all goods
        self.finalPrices = kwargs.get('finalPrices')
        
        self.pricePrediction = kwargs.get('pricePrediction')
        
        super(simYW,self).__init__(**kwargs)
        
    @staticmethod
    def randomValueVector(vmin = 1, vmax = 50, m = 5, l = None):
        if l is None:
            l = numpy.random.random_integers(low = 1, high = m)
            
        v = numpy.zeros(m)
        
        sortedRandInts = numpy.random.random_integers(low = vmin, high=vmax, size = (m-l+1))
        sortedRandInts.sort()
        sortedRandInts = sortedRandInts[::-1]
        
        v[(l-1):] = sortedRandInts
    
        return v, l 
    
    def randomValuation(self, *args, **kwargs):
        """
        Draw a new valuation function given the agent's parameters.
        """
        vmin = kwargs.get('vmin',self.vmin)
        vmax = kwargs.get('vmax',self.vmax)
        m    = kwargs.get('m',self.m)
        l    = kwargs.get('l')
        
        self.v, self.l = simYW.randomValueVector(vmin, vmax, m, l)
        
            
    def acq(self, **kwargs):
        """
        Calculate the optimal bundle for this class instance.
        """
        priceVector = kwargs['priceVector']
        bundles = simYW.allBundles(self.m)
        valuation = simYW.valuation(bundles,self.v,self.l)
        return simYW.acqYW(bundles     = bundles,
                           valuation   = valuation,
                           priceVector = priceVector,
                           l           = self.l)
    
    @staticmethod
    def minMaxHelper(_bundles, _utility, _l):
        if _bundles.shape[0] == 1:
        #if there is one bundle and utility
            _optBundle   = _bundles[0]
            _optUtility  = _utility[0]
            return _optBundle, _optUtility
        else:
            t = numpy.float('inf')
            _optBundle  = None
            _optUtility = None
            for idx in xrange(_bundles.shape[0]):
                tempBinList = _bundles[idx]
                cs          = numpy.cumsum(tempBinList)
                tNew        = (numpy.array(cs) >= _l).nonzero()
                if tNew[0].any():
                    tNew = tNew[0][0]
                    if tNew < t:
                        t = tNew
                        _optBundle        = _bundles[idx]
                        _optUtility       = _utility[idx]
                        
            return _optBundle, _optUtility
    
    @staticmethod
    def minMaxBundle(**kwargs):
        """
        A function to compute the "minimal" bundle given a list of
        bundles.
        
        If there are bundles with equal "value" to the agent pick the one
        that completes the tasks first, e.g.
        
        if $\lambda$ = 2 and m = 5 [1 1 0 0 0 ] should be prefered to [1 0 0 0 1]
        given both have equal utility
        """
        #will raise assertions if not in kwargs
        bundles = numpy.atleast_2d(kwargs['bundles'])
        utility    = numpy.atleast_1d(kwargs['utility'])
        
        numpy.testing.assert_equal(bundles.shape[0], utility.shape[0],
                                   err_msg="Each bundle must have a corresponding utility.")
        
        optBundle = None
        optUtility = None
        
        if 'l' in kwargs:
            optBundle, optUtility = simYW.minMaxHelper(bundles,utility,kwargs['l'])
            if optBundle == None:
                #return the minimum bundle that finishes earliest
                lmin = numpy.min([numpy.sum(bundles[bundleIdx]) for bundleIdx in xrange(bundles.shape[0])])
                optBundle, optUtility = simYW.minMaxHelper(bundles,utility,lmin)
        else:
            #pick the smallest bundle that finishes first
            lmin = numpy.min([numpy.sum(bundles[bundleIdx]) for bundleIdx in xrange(bundles.shape[0])])
            optBundle,optUtility = simYW.minMaxHelper(bundles,utility,lmin)
            
             
        return numpy.atleast_1d(optBundle).astype(bool), optUtility      
        

    def printSummary(self, **kwargs):
        """
        Print a summary of agent state to standard out.
        """
        print "Agent Name:              {0}".format(self.name)
        print "Agent ID:                {0}".format(self.id)
        print "Agent Type:              {0}".format(self.type())
        print "Agent lambda           = {0}".format(self.l)
        print "Agent Valuation Vector = {0}".format(self.v)
        
    @staticmethod
    def SS(self,**kwargs):
        """
        An agents' strategy profile. Computes the optimal bid given the
        agent's status and arguments to SS. Should be implmented for each
        agent type.
        
        Should be given the bundles to bid on, the valuation for each bundle
        and any other relavant information for the concrete agent type.
        """
        print "Cannot Bid with abstract simYW."
        print "Please instantiate a concrete agent"
        raise AssertionError
    
    def bid(self, **kwargs):
        """
        An interface to trigger the agent to bid.
        Though this function should be called to return a specific agent's bid,
        the bid is computed using the agent's strategy profile class.SS(self, args={})
        which can be called with arbitrary arguments.
        """
        print "Cannot Bid with abstract simYW."
        print "Please instantiate a concrete agent"
        raise AssertionError
        
    @staticmethod
    def allBundles(nGoods = 5):
        """
        Return a numpy 2d array of all possible bundles that the agent can
        bid on given the number of auctions.
        
        The Rows represent the bundle index.
        
        The Columns Represent the good index.        
        
        Return bundles as booleans for storage and computational efficiency
        """
        assert isinstance(nGoods,int) and nGoods >=0,\
            "nGoods = {0} is not a positive integer".format(nGoods)
        return numpy.atleast_2d([bin for bin in itertools.product([False,True],repeat=nGoods)]).astype(bool)
    
#    @staticmethod
#    def bundleGenerator(nGoods = 5):
#        for bin in itertools.product([False,True],repeat = nGoods):
#            yield bin
        
    
    
    @staticmethod
    def valuation(bundles = None, v = None, l= None):
        """
        Calculate the valuation of a given list of bundles
        """
        numpy.testing.assert_(isinstance(bundles,numpy.ndarray) or\
                              isinstance(bundles,list), 
                              msg="bundles must be a list or numpy.ndarray")
        
        numpy.testing.assert_(isinstance(v,numpy.ndarray),
                              msg="v must be a numpy.ndarray")
        
        assert isinstance(l,int) and l >= 0 and l <= v.shape[0],\
            "simYW::valuation l = {0} must be a positive integer "+\
            "which is smaller than the size of v = {1}".format(l,v)
            
            
        bundles = numpy.atleast_2d(bundles)
        
        cs = [numpy.atleast_1d(i) for i in itertools.imap(numpy.cumsum,bundles)]
        
        valuation = []
        for bundle in cs:
            if bundle[-1] < l:
                valuation.append(0)
            else:
                t = numpy.nonzero(bundle >= l)[0][0]
                valuation.append(v[t])
                
        return numpy.atleast_1d(valuation)
        
    @staticmethod
    def cost(bundles = None, price = None):
        """
        A function to calculate the cost for a given set of bundles and prices
        """
               
        bundles = numpy.atleast_2d(bundles)
        price = numpy.atleast_1d(price)
        
        assert price.shape[0] == bundles.shape[1],\
        "simYW::cost price.shape[0] = {0} != bundles.shape[1] = {1}".format(price.shape[0],bundles.shape[1])
        
        if price.dtype != numpy.dtype('float'):
            price = price.astype(numpy.float)
            
        if (price == float('inf')).any():
            # if there are items which are unobtainable (cost = inf)
            # then the cost for the bundles containing that good should
            # be inf but the bundles not containing those goods should be the 
            # cost of other goods
            
            # lists are mutable, deep copy the original price vector
            # in order to preserve the argument
            
            unobtainableGoods = numpy.nonzero(price == float('inf'))[0]
             # make a deep copy so not to mutate func. argument
            priceInfZero = numpy.atleast_1d(numpy.array(price))
            priceInfZero[unobtainableGoods] = 0
            
            cost = []
            for idx in xrange(bundles.shape[0]):
                if (bundles[idx][unobtainableGoods] == 0).all():
                    cost.append(numpy.dot(bundles[idx],priceInfZero))
                else:
                    cost.append(float('inf'))
                    
            return numpy.atleast_1d(cost)
        else:
            return numpy.atleast_1d([numpy.dot(bundle,price) for bundle in bundles])
        

        
    @staticmethod
    def surplus(bundles=None, valuation = None, priceVector = None):
        """
        Calculate the surplus for a given array of bundles, prices and a valuation (scalar).
        Surplus equals valuation less cost.
        """
                   
        bundles = numpy.atleast_2d(bundles)
        
        valuation = numpy.atleast_1d(valuation)
        
        return valuation - simYW.cost(bundles = bundles, price = priceVector)
    
    def expectedValuation(self,**kwargs):
        pricePrediction = kwargs.get('pricePrediction', self.pricePrediction)
        bundles         = kwargs.get('bundles',simYW.allBundles(self.m))
        v               = kwargs.get('v',self.v)
        l               = kwargs.get('l',self.l)
        val             = kwargs.get('valuation',self.valuation(bundles, v, l))
        bids            = kwargs.get('bids', self.bid(pricePrediction = pricePrediction))
        
        ev = pricePrediction.expectedValuation(bundles, val, bids)
        
        return ev
    
    def expectedCost(self,**kwargs):
        pricePrediction = kwargs.get('pricePrediction', self.pricePrediction)
        bundles         = kwargs.get('bundles', simYW.allBundles(self.m))
        v               = kwargs.get('v',self.v)
        l               = kwargs.get('l',self.l)
        val             = kwargs.get('valuation',self.valuation(bundles, v, l))
        bids            = kwargs.get('bids',self.bid(pricePrediction = pricePrediction))
        qmin            = kwargs.get('qmin',0)
        qstep           = kwargs.get('qstep',1)
        
        ec = pricePrediction.expectedCost(bundles,val,bids,qmin,qstep)
        
        return ec
    
    def expectedUtility(self,**kwargs):
        ev = self.expectedValuation(**kwargs)
        ec = self.expectedCost(**kwargs)
        u = ev - ec
        return u
        
        

    
    def finalSurplus(self):
        numpy.testing.assert_(isinstance(self.bundleWon,numpy.ndarray),
            msg="invalid self.bundleWon")
        
        numpy.testing.assert_(isinstance(self.finalPrices,numpy.ndarray),
            msg="invalid self.finalPrices")
        
        return self.surplus(self.bundleWon, 
                            self.valuation(self.bundleWon, self.v, self.l),
                            self.finalPrices)[0]
    
    @staticmethod
    def idx2bundle(index=None, nGoods = 5):
        # convert to decimal rather than enumerating power set
        # and selecting correct bundle
        
        assert index != None and nGoods != None,\
            "simYW::bundleFromIndex must specify all arguments."
            
        assert isinstance(index,int) and index >= 0,\
            "simYW::bundleFromIndex index must be a positive integer."
            
        assert isinstance(nGoods,int) and nGoods >0,\
            "simYw::bundleFromIndex nGoods must be a strictly positive integer."
        
        binList = []
        n = index
        while n > 0:
            binList.insert(0,n%2)
            n = n >> 1
            
        # just checking the index wasn't
        # past the maximum bundle
        if len(binList) > nGoods: raise ValueError, "simYW::bundleFromIndex Error: Dec-Binary Conversion"
        
        for i in xrange(nGoods-len(binList)):
            binList.insert(0,0)
            
        return numpy.atleast_1d(binList)
    
    @staticmethod
    def bundle2idx(bundle = None):
        numpy.testing.assert_(bundle.dtype == bool,
                              msg="bundle.dtype = {0} != bool".format(bundle.dtype))
        idx = 0
        for i in xrange(bundle.shape[0]):
            idx = (2**((bundle.shape[0]-1)-i))*bundle[i]
            
        return idx
    
    @staticmethod
    def acqYW(**kwargs):
#    def acqYW(bundles = None, valuation = None, l = None, priceVector = None):
        """
        Given the number of goods, a price vector over each good
        and a valuation for each good, compute the optimal acquisition
        as described in Boyan and Greenwald 2001.
        
        INPUTS:
            bundles       :=     a numpy 2d array
                                 rows indicate individual bundles
                                 columns are individual goods
                                 
            priceVector   :=     vector of prices over goods.
                                 priceVector.shape[0] == bundles.shape[1] == number of goods
            
            valuation     :=     an numpy array of valuations, one for each bundle
        
        """    
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("simYW.acqYW(...) - Must specify possible bundles")
        
        bundles = numpy.atleast_2d(bundles)
        
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("simYW.acqYW(...) - Must specify valuation vector")
        
        valuation = numpy.atleast_1d(valuation)
                                     
        priceVector = kwargs.get('priceVector')
        if priceVector == None:
            raise KeyError("simYW.acqYW(...) - Must specify valuation")
        
        priceVector = numpy.atleast_1d(priceVector)
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("simYW.acqYW(...) - Must specify l (number of target goods")
        
        surplus = numpy.atleast_1d( kwargs.get('surplus', simYW.surplus(bundles     = bundles,
                                                                        valuation   = valuation,
                                                                        priceVector = priceVector)) )        
        
        # there may be more than one "optimal bundles" i.e. bundles with
        # the same maximal surplus
        optBundleIdxList = numpy.nonzero(surplus == numpy.max(surplus))[0]
        
        return simYW.minMaxBundle(bundles = bundles[optBundleIdxList],
                                  utility = surplus[optBundleIdxList],
                                  l       = l)
        
    @staticmethod
    def marginalUtility(bundles, priceVector, valuation, l, goodIdx):
#        priceVector = numpy.atleast_1d(priceVector)
        priceVector = numpy.asarray(priceVector,dtype = numpy.float)
        
        tempPriceInf = priceVector.copy()
        tempPriceInf[goodIdx] = numpy.float('inf')
        
        tempPriceZero = priceVector.copy()
        tempPriceZero[goodIdx] = numpy.float(0.0)
        

        optBundleInf, predictedSurplusInf = simYW.acqYW(bundles     = bundles,
                                                        valuation   = valuation,
                                                        l           = l,
                                                        priceVector = tempPriceInf)
            
        optBundleZero, predictedSurplusZero = simYW.acqYW(bundles     = bundles,
                                                          valuation   = valuation,
                                                          l           = l, 
                                                          priceVector = tempPriceZero)
    
    
        margUtil = predictedSurplusZero - predictedSurplusInf
        if margUtil < 0:
            raise ValueError("simYW.marginalUtility(...) - Negative Marginal Utility (shouldn't happen).")
        
        return margUtil
            
    def validatePriceVector(self,priceVector):
        """
        Return true if a given list of prices is compatible with this agent's functions.
        """
        pv = numpy.atleast_2d(priceVector)
        
        assert pv.shape[0] == 1,\
            "Must specify 1d price vector"
            
        assert pv.shape[1] == self.m,\
            "priceVector.shape[1] = {0} != self.m = {1}.".format(pv.shape[1],self.m)
            
        return True
            
    @staticmethod
    def type():
        return "simYW"
        