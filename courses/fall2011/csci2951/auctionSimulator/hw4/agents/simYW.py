"""
This is /auctionSimulator/hw4/agents/simYW.py

Author:    Brandon A. Mayer
Date:      11/26/2011

A base class for agents who participate in simultaneous auctions of the type
described by Yoon & Wellman 2011
"""

from auctionSimulator.hw4.agents.agentBase import *

import itertools
import numpy

class simYW(agentBase):
    """
    Base class for agents competing in the auction for time slots described by
    Yoon & Wellman 2011.
    
    Note: 
        I made the functions:
                        allBundles
                        valuation
                        cost
                        surplus
                        bundleFromIndex
                        
        static functions on purpose to keep the class light. I wanted the
        class to store the data specific to the Yoon & Wellman specification as
        well as have the functions necessary to manipulate these data but I didn't
        feel these funcitons should be attached to every class instance.
    """
    
    def __init__(self, 
                 m = 5, 
                 l = None, 
                 v = None,
                 vmin=0,
                 vmax=50, 
                 name="Anonymous"):
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
        self.m = m
        
        
        if l == None:
            self.l = numpy.random.random_integers(low=1,high=m)
        else:
            assert isinstance(l,int),\
                "parameter l must be an integer number of slots."
            self.l = l
        
        if v == None:
            self.v = numpy.random.random_integers(low=vmin,high=vmax,self.m)
            self.v.sort() 
            #sort is in ascending order, 
            #switch around for descending
            self.v = self.v[::-1]
        else:
            if self.m == 1:
                assert isinstance(v,int),\
                    "For an auction with 1 slot, the valuation must be for 1 slot."
            else:
                v = numpy.atleast_1d(v)
                
                assert v.shape[0] == self.m,\
                    "v.shape[0] = {0} must equal self.m = {1}".format(v.shape[0],self.m)
                                 
            self.v = numpy.atleast_1d(v)
        
        super(simYW,self).__init__(name)
        
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
            "nGoods must be a positive integer"
        return numpy.atleast_2d([bin for bin in itertools.product([False,True],repeat=setLength)]).astype(bool)
    
    
    @staticmethod
    def valuation(bundles, v, l):
        """
        Calculate the valuation of a given list of bundles
        """
        assert isinstance(bundles,numpy.ndarray),\
            "simYW::valuation bundles must be a numpy.ndarray"
            
        assert isinstance(v, numpy.ndarray),\
            "v must be a numpy.ndarray"
        
        assert isinstance(l,int) and l >= 0 and l < v.shape[0],\
            "simYW::valuation l must be a positive integer which is smaller than the size of v"
            
            
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
    def cost(bundles, price):
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
    def surplus(bundles=None, price=None, v=None, l=None):
        """
        Calculate the surplus for a given array of bundles, prices and a valuation vector.
        Surplus equals valuation less cost.
        """
        assert bundles != None and\
               price != None and\
               v != None and\
               l != None,\
               "simYW::surplus must specify all parameters"
        return numpy.atleast_1d([c for c in itertools.imap(operator.sub,simYW.valuation(bundles=bundles, v=v, l=l), simYW.cost(bundles=bundles, price=price))])
    
    @staticmethod
    def bundleFromIndex(index=None, nGoods = 5):
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
        if len(binList) > self.m: raise ValueError, "simYW::bundleFromIndex Error: Dec-Binary Conversion"
        
        for i in xrange(nGoods-len(binList)):
            binList.insert(0,0)
            
        return numpy.atleast_1d(binList)
        
        
        
    
    
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
        