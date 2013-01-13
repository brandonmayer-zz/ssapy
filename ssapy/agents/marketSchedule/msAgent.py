import numpy
import itertools

from ...agents import agentBase

from ...util import listBundles as listBundles_
from ...util import cost as cost_
from ..marketSchedule import listRevenue as listRevenue_
from ..marketSchedule import randomValueVector as randomValueVector_
from ..marketSchedule import dictRevenue as dictRevenue_

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
        self.m = kwargs.get('m')
        
        self.l = kwargs.get('l',numpy.random.random_integers(low = 1, high = self.m))     
        
        self.vmin = kwargs.get('vmin',0)
            
        self.vmax = kwargs.get('vmax',50)   
        
        self.pricePrediction = kwargs.get('pricePrediction')
                
        self.v = kwargs.get('v')
        
        if self.m == None and self.v == None:
            raise ValueError("msAgent.__init__ - must specify either v or m")
        elif self.m == None and self.v != None:
            self.m = len(self.v)
        elif self.v == None:
            self.v = randomValueVector_(vmin = self.vmin, 
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
        
        self.v, self.l = randomValueVector_(vmin, vmax, m, l)
        
#    def revenue(self):
#        return listRevenue(bundles, v, l)
#    
#    def bundles(self):
#        return listBundles(self.m)               
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
        
        rev = listRevenue_(self.bundleWon, self.v, self.l)
        
        c = cost_(self.bundleWon, self.finalPrices)
        
        return rev - c
  
    def listRevenue(self):
        return listRevenue_(self.listBundles(), self.v, self.l)
        
    def dictRevenue(self):
        return dictRevenue_(self.v, self.l)
        
    def listBundles(self):
        return listBundles_(self.m)
        
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
        return "msAgent"