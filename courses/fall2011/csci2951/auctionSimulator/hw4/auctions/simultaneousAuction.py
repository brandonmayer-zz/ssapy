"""
This is /auctionSimulator/hw4/simultaneousAuction
Aution:    Brandon A. Mayer
Date:      12/2/2011

A class implementing a simultaneous auction.
"""
from auctionSimulator.hw4.agents.agentBase import *
from auctionBase import *


import numpy
import heapq

class simultaneousAuction(auctionBase):
    """
    A class for simulating simultaneous one shot auctions.
    """
    def __init__(self, agentList = [], m = 5, nPrice = 2, name='simultaneousAuction', reserve = 0):
        
        
        self.setAgentList(agentList=agentList)
        
        super(simultaneousAuction,self).__init__(name)
        
        self.m          = int(m)
        self.nPrice     = int(nPrice)
        self.reserve    = reserve
        
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
            
    def runAuction(self,args={}):
        
        nPrice = None
        if 'nPrice' in args:
            nPrice = args['nPrice']
        else:
            nPrice = self.nPrice
            
        reserve = None
        if 'reserve' in args:
            reserve = args['reserve']
        else:
            reserve = self.reserve
            
        #collect the bids from the agents
        bids = numpy.atleast_2d([agent.bid(args) for agent in self.agentList])
        
        # numpy.argmax(2darray,0) returns the argmax over columns
        winners = numpy.argmax(bids,0).astype(numpy.float)
        
        winningBids = numpy.max(bids,0)
        
        #don't give away an item for free
        winners[winningBids == 0] = numpy.nan
        
        winners[winningBids < self.reserve] = numpy.nan
        
        #if the winning bids are not greater than the reserve,
        finalPrices = numpy.atleast_1d([sorted(bids[:,i],reverse=True)[nPrice] for i in xrange(bids.shape[1])])
        
        finalPrices[finalPrices < reserve] = reserve
        
        self.winners = winners
        
        self.finalPrices = finalPrices
        
        self.winningBids = winningBids
        
        return winners, finalPrices, winningBids      
    
    def notifyAgents(self,args={}):
        """
        Will modify all agent's agent.bundleWon and agent.finalPrices member variables
        so agents individual know which bundles they have obtained and
        at what price
        """
        #iterate through agents
        for agentIdx in xrange(len(self.agentList)):
            
            #initialize agent's bundle notifications to zeros of appropriate shape
            self.agentList[agentIdx].bundleWon = numpy.zeros(self.winners.shape[0])
            
            #let agent know of all final prices
            self.agentList[agentIdx].finalPrices = self.finalPrices
            
            #if self.winner is the agent index, set the agent's
            #bundleWon to 1 for those goods
            self.agentList[agentIdx].bundleWon[self.winners == agentIdx] = 1   
            
    def agentSurplus(self,args={}):
        return numpy.atleast_1d([agent.finalSurplus() for agent in self.agentList])