"""
this is /auctionSimulator/hw4/baselineBidder.py

Author: Brandon Mayer
Date: 11/17/2011

Specialized agent class to replicate baselineBidding from
Yoon and Wellman (2011)
"""
from simYW import *

class baselineBidder(simYW):
    """
    Replicated BaselineBidding agent from Yoon & Wellman 2011
    """
        
    def type(self):
        return "baselineBidder" 
    
    def printSummary(self,args={}):
        """
        Print a summary of the class instance
        """
        super(baselineBidder,self).printSummary()
        
        print"Bid:     {0}".format(self.bid())
        
    def bid(self,args={}):
        """
        "BaselineBidding agents with a 
        single-unit task bid true value for the first slot, and otherwise they bid
        for the first \lambda_i goods at price v_i^(\labmda_i)/(\lambda_i)" 
        (Yoon & Wellman, 2011)
        
        NOTE: 
            Base line bidder does not solve for a target bundle to bid (acq) 
            it just bids for the first self.l items at a price of excess value
            distributed normally over the set of goods
        """
        bid = []
        
        for i in range(self.m):
            if i < self.l:
                bid.append(float(self.v[self.l-1])/self.l)
            else:
                bid.append(0)
                      
        return numpy.array(bid)   