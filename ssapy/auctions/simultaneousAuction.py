"""
This is /auctionSimulator/hw4/simultaneousAuction
Aution:    Brandon A. Mayer
Date:      12/2/2011

A class implementing a simultaneous auction.
"""
from ssapy.agents import agentBase
from ssapy.auctionBase import *


import numpy
import heapq

class simultaneousAuction(auctionBase):
    """
    A class for simulating simultaneous one shot auctions.
    """
    def __init__(self,**kwargs):
        agentList = kwargs.get('agentList', [])
        
        self.setAgentList(agentList=agentList)
        
        self.m       = kwargs.get('m', 5)
        self.nPrice  = int(kwargs.get('nPrice', 2))
        self.reserve = kwargs.get('reserve',0)
        
        #indicate the auction has not yet run
        self.finalPrices = None
        self.winners     = None
        self.winningBids = None
        
        super(simultaneousAuction,self).__init__(**kwargs)
        
    @staticmethod
    def type():
        return 'simultaneousAuction'
        
    def setAgentList(self, agentList = []):
        """
        Replace the current agent list with a single or list of agents.
        """
        numpy.testing.assert_(isinstance(agentList,list) 
                                or isinstance(agentList,agentBase), 
                              msg = "agentList must be a list of or a single agentBase")
        
        if isinstance(agentList,agentBase):
            for agent in agentList:
                numpy.testing.assert_(isinstance(agent,agentBase),
                                      msg = "Agents must be subtype of agentBase")
            
        self.agentList = agentList
        
    def attachAgents(self, agentList = []):
        """
        Add one or more agent to the list of participating agents.
        """        
        if isinstance(agentList,list):
            for agent in agentList:
                numpy.testing.assert_(isinstance(agent,agentBase))
                self.agentList.append(agent)
        elif instance(agentList,agentBase):
            self.agentList.append(agentBase)
        else:
            print 'Must specify a list of agents of subtype agentBase or a single such agent.'
            raise AssertionError
        
    def removeAgent(self,agentId):
        """
        Remove an attached agent with a given id.
        """
        targetAgent = filter(lambda agent: agent.id == agentId, self.agentList)
        #each id should be unique so the targetAgent will be a list with one element
        if targetAgent:
            self.agentList.remove(targetAgent[0])
            
    def runAuction(self,**kwargs):
        
        nPrice  = kwargs.get('nPrice', self.nPrice)
        
        reserve = kwargs.get('reserve', self.reserve)
            
        #collect the bids from the agents
        bids = numpy.atleast_2d([agent.bid(**kwargs) for agent in self.agentList])
        
        # the highest bids
        winningBids = numpy.max(bids,0)
        
        # if there is more than one agent bidding the highest price
        # pick the winner at random.
        winners = numpy.zeros(bids.shape[1],dtype=numpy.float)
        for m in xrange(bids.shape[1]):
            maxBids = numpy.nonzero(bids[:,m] == numpy.max(bids[:,m]))[0]
            if maxBids.shape[0] > 1:
                numpy.random.shuffle(maxBids)        
            winners[m]=maxBids[0]
                
        
        # numpy.argmax(2darray,0) returns the argmax over columns
#        winners = numpy.argmax(bids,0).astype(numpy.float)
        
        #don't give away an item for free
        winners[winningBids == 0] = numpy.nan
        
        winners[winningBids < self.reserve] = numpy.nan
        
        #if the winning bids are not greater than the reserve,
        finalPrices = numpy.atleast_1d([sorted(bids[:,i],reverse=True)[nPrice-1] for i in xrange(bids.shape[1])])
        
        finalPrices[finalPrices < reserve] = reserve
        
        self.winners = winners
        
        self.finalPrices = finalPrices
        
        self.winningBids = winningBids
        
        return winners, finalPrices, winningBids      
    
    def notifyAgents(self,**kwargs):
        """
        Will modify all agent's agent.bundleWon and agent.finalPrices member variables
        so agents individual know which bundles they have obtained and
        at what price
        """
        
        numpy.testing.assert_(self.finalPrices != None,
            msg="self.finalPrices are not yet valid.")
        
        numpy.testing.assert_(self.winners != None,
            msg="self.winners is not yet valid.")
        
        numpy.testing.assert_(self.winningBids != None,
            msg="self.winningBids is not yet valid.")
        
        #iterate through agents
        for agentIdx in xrange(len(self.agentList)):
            
            #initialize agent's bundle notifications to zeros of appropriate shape
            self.agentList[agentIdx].bundleWon = numpy.zeros(self.winners.shape[0])
            
            #if self.winner is the agent index, set the agent's
            #bundleWon to 1 for those goods
            self.agentList[agentIdx].bundleWon[self.winners == agentIdx] = 1   
            
            #let agent know of all final prices
            self.agentList[agentIdx].finalPrices = self.finalPrices
                 
    def agentSurplus(self,**kwargs):
        return numpy.atleast_1d([agent.finalSurplus() for agent in self.agentList])