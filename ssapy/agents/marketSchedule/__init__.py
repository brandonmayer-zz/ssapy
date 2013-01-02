"""
this is /ssapy/marketSchedule/__init__.py

Author: Brandon A. Mayer
Date: 1/1/2013

Module for Market Scheduling Game functions and agents as described in:

"Exploring bidding strategies for market-based scheduling", Reeves et. al. 2005 

and

"Self-Confirming Price-Prediction Strategies for Simultaneous One-Shot Auctions",
Yoon et. al. 2007
"""
import numpy
import itertools

from ssapy.agents import agentBase
from ssapy.util import listBundles, cost


def randomValueVector(vmin = 1, vmax = 50, m = 5, l = None):
    if l is None:
        l = numpy.random.random_integers(low = 1, high = m)
        
    v = numpy.zeros(m)
    
    sortedRandInts = numpy.random.random_integers(low = vmin, high=vmax, size = (m-l+1))
    sortedRandInts.sort()
    sortedRandInts = sortedRandInts[::-1]
    
    v[(l-1):] = sortedRandInts

    return v, l 

def listRevenue(bundles, v, l):
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
    if bundles == None:
        bundles = listBundles(numpy.atleast_1d(v).shape[0])
    else:
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

def revenueDict(v, l):
    
    m = numpy.asarray(v).shape[0]
    
    rev = {}
    
    for bundle in listBundles(m):
        cs = numpy.cumsum(bundle)
        if cs[-1] < l:
            rev[tuple(bundle)] = 0
        else:
            t = numpy.nonzero(bundle >= l)[0][0]
            rev[tuple(bundle)] = v[t]
            
    return rev


class msAgent(agentBase):
    """
    Base class for agents competing in the auction for time slots described by
    Yoon & Wellman 2007 and Reeves 2005.
    """
    
    def __init__(self, **kwargs):
        """
            INPUTS:
                strategy     := a string specifying the bidding strategy
                
                m            := the total number of time slots up for auction
                
                l            := the target number of time slots for the specific agent
                                chosen at random from 0->m if not specified
                                
                v            := list of valuations for time slots. Must be of size m
                                chosen at random by same random procedure
                                as Yoon & Wellman if not specified
                
                v_min        := the minimum valuation for a time slot
                
                v_max        := the maximum valuation for a time slot
                
            NOTES:
                Though an explicit array of possible bundles isn't stored,
                we can imagine that there exists a list of bundles, each
                is a binary vector where a 1 in the t^th position indicates that the
                t^th good is included in the bundle. 
                
                If we were to enumerate all bundles, we could count from 0->(self.l-1) 
                e.g. self.l = 3 implies a list of
                [0, 0, 0]
                [0, 0, 1]
                ...
                [1, 1, 1]
                
                Assume big Endianness; the msb of the binary representation indicates
                slot one the lsb is then the (self.m - 1)^st good
                
                e.g. [1,0,0] is a bundle containing the first slot and has an index into our "virtual"
                bundle list of 4.
                
                If we want to convert an index into a bundle, just convert the index to binary
                and create the appropriately sized list, padding with zeros as necessary and 
                dictated by self.m
                
                1/1/2013:
                    bundle2idx and idx2bundle have been moved ssapy.util as they are 
                    useful in a general auction setting not only to market scheduling.
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
                
    def printSummary(self, **kwargs):
        """
        Print a summary of agent state to standard out.
        """
        print "Agent Name:              {0}".format(self.name)
        print "Agent ID:                {0}".format(self.id)
        print "Agent Type:              {0}".format(self.type())
        print "Agent lambda           = {0}".format(self.l)
        print "Agent Valuation Vector = {0}".format(self.v)
    
    
    def finalSurplus(self):
        numpy.testing.assert_(isinstance(self.bundleWon,numpy.ndarray),
            msg="invalid self.bundleWon")
        
        numpy.testing.assert_(isinstance(self.finalPrices,numpy.ndarray),
            msg="invalid self.finalPrices")
        
        rev = listRevenue(self.bundleWon, self.v, self.l)
        
        c = cost(self.bundleWon, self.finalPrices)
        
        return rev - c
  
                
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
    