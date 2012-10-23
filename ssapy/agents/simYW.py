"""
This is /auctionSimulator/hw4/agents/simYW.py

Author:    Brandon A. Mayer
Date:      11/26/2011

A base class for agents who participate in simultaneous auctions of the type
described by Yoon & Wellman 2011
"""
from agentBase import *
import ssapy
import itertools
import numpy

def randomValueVector(vmin = 1, vmax = 50, m = 5, l = None):
    if l is None:
        l = numpy.random.random_integers(low = 1, high = m)
        
    v = numpy.zeros(m)
    
    sortedRandInts = numpy.random.random_integers(low = vmin, high=vmax, size = (m-l+1))
    sortedRandInts.sort()
    sortedRandInts = sortedRandInts[::-1]
    
    v[(l-1):] = sortedRandInts

    return v, l 

def valuation(bundles, v, l):
    """Compute the revenue (valuation) for a given list of bundles (collection of goods)
    
    Parameters
    ----------
    bundles: array_like, shape (n_bundles, n_goods)
        List of collection of goods. Each row is collection, each column a good index.
        A 1 in the i^{th} row and j^{th} column implies the good j is contained in the 
        i^{th} listed bundle.
    
    v: array_like, shape (n_goods)
        The value vector described in the Market Scheduling game of YW.
        
    l: int,
        The minimal number of goods the agent needs to win to obtain value.
        Another parameter of the market schedule game.
        
    Returns
    -------
    valution: array_like, shape (n_bundles)
        valution[i] is the revenue the agent would receive had
        he/she been able to procure the collection of goods bundle[i]. 
    """
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
        
        self.pricePrediction = kwargs.get('pricePrediction')
        
        if 'v' in kwargs:    
            self.v = numpy.atleast_1d(kwargs['v'])
            numpy.testing.assert_equal(self.v.shape[0], self.m,
                                       err_msg="self.v.shape[0] = {0} != self.m = {1}".format(self.v.shape[0],self.m))
        else:
            self.v = randomValueVector(vmin = self.vmin, 
                                       vmax = self.vmax, 
                                       m    = self.m,
                                       l    = self.l)[0]
            
        # a bit vector indicating which items where won
        # at auction
        self.bundleWon = None
        
        # a vector of final prices for all goods
        self.finalPrices = None
        
        super(simYW,self).__init__(**kwargs)
        
    
    
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
        bundles = simYW.allBundles(self.m)
        valuation = simYW.valuation(bundles,self.v,self.l)
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
#        print "Cannot Bid with abstract simYW."
#        print "Please instantiate a concrete agent"
#        raise AssertionError
        m                  = kwargs.get('m', self.m)
        v                  = kwargs.get('v', self.v)
        l                  = kwargs.get('l', self.l)
        pricePrediction    = kwargs.get('pricePrediction', self.pricePrediction)
        bundles            = kwargs.get('bundles', ssapy.allBundles(m))
        
        return self.SS( pricePrediction = pricePrediction,
                        bundles         = bundles,
                        l               = l,
                        valuation       = valuation(bundles, v, l))  
    
    def finalSurplus(self):
        numpy.testing.assert_(isinstance(self.bundleWon,numpy.ndarray),
            msg="invalid self.bundleWon")
        
        numpy.testing.assert_(isinstance(self.finalPrices,numpy.ndarray),
            msg="invalid self.finalPrices")
        
        return ssapy.surplus(self.bundleWon, 
                             valuation(self.bundleWon, self.v, self.l),
                             self.finalPrices)[0]
  
                
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
        