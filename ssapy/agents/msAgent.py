"""
This is /auctionSimulator/hw4/agents/simYW.py

Author:    Brandon A. Mayer
Date:      11/26/2011

A base class for agents who participate in simultaneous auctions of the type
described by Yoon & Wellman 2011
"""
import ssapy
from agentBase import agentBase
from ssapy.marketSchedule import randomValueVector, listRevenue

import numpy


class msAgent(agentBase):
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
                strategy     := a string specifying the bidding strategy
                
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
        
        self.pricePrediction = kwargs.get('pricePrediction')
                
        self.v = kwargs.get('v')
        
        if self.v == None:
            self.v = randomValueVector(vmin = self.vmin, 
                                       vmax = self.vmax, 
                                       m    = self.m,
                                       l    = self.l)[0]
        else:
            self.v = numpy.atleast_1d(self.v)
            numpy.testing.assert_equal(self.v.shape[0], self.m,
                                       err_msg="self.v.shape[0] = {0} != self.m = {1}".\
                                       format(self.v.shape[0],self.m))
             
        super(msAgent,self).__init__(**kwargs)
    
    def randomValuation(self, *args, **kwargs):
        """
        Draw a new valuation function given the agent's parameters.
        """
        vmin = kwargs.get('vmin',self.vmin)
        vmax = kwargs.get('vmax',self.vmax)
        m    = kwargs.get('m',self.m)
        l    = kwargs.get('l')
        
        self.v, self.l = randomValueVector(vmin, vmax, m, l)
        
            
    def acq(self, **kwargs):
        """
        Calculate the optimal bundle for this class instance.
        """
        priceVector = kwargs['priceVector']
        bundles = ssapy.allBundles(self.m)
        valuation = listRevenue(bundles,self.v,self.l)
        return ssapy.acq(bundles     = bundles,
                         valuation   = valuation,
                         priceVector = priceVector )
                     
        
    def printSummary(self, **kwargs):
        """
        Print a summary of agent state to standard out.
        """
        print "Agent Name:              {0}".format(self.name)
        print "Agent ID:                {0}".format(self.id)
        print "Agent Type:              {0}".format(self.type())
        print "Agent lambda           = {0}".format(self.l)
        print "Agent Valuation Vector = {0}".format(self.v)
    
#    def bid(self, **kwargs):
#        """
#        An interface to trigger the agent to bid.
#        Though this function should be called to return a specific agent's bid,
#        the bid is computed using the agent's strategy profile class.SS(self, args={})
#        which can be called with arbitrary arguments.
#        """
##        print "Cannot Bid with abstract simYW."
##        print "Please instantiate a concrete agent"
##        raise AssertionError
#
#        
#        strategy = kwargs.get('strategy',self.strategy)
#        
#        if strategy == None:
#            raise ValueError("Must Specify Strategy")
#        
#        elif isinstance(strategy,str):
#            strategy = ssapy.getStrategy(strategy)
#            
#        m                  = kwargs.get('m', self.m)
#        v                  = kwargs.get('v', self.v)
#        l                  = kwargs.get('l', self.l)
#        pricePrediction    = kwargs.get('pricePrediction', self.pricePrediction)
#        bundles            = kwargs.get('bundles', ssapy.allBundles(m))
#        
#        
#        return strategy(pricePrediction = pricePrediction,
#                        bundles         = bundles,
#                        valuation       = valuation(bundles,v,l))
    
    def finalSurplus(self):
        numpy.testing.assert_(isinstance(self.bundleWon,numpy.ndarray),
            msg="invalid self.bundleWon")
        
        numpy.testing.assert_(isinstance(self.finalPrices,numpy.ndarray),
            msg="invalid self.finalPrices")
        
        return ssapy.surplus(self.bundleWon, 
                             listRevenue(self.bundleWon, self.v, self.l),
                             self.finalPrices)
  
                
    def validatePriceVector(self, priceVector):
        """
        Return true if a given list of prices is compatible with this agent's state.
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
        