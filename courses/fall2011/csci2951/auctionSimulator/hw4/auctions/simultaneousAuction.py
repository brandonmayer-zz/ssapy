"""
This is /auctionSimulator/hw4/simultaneousAuction
Aution:    Brandon A. Mayer
Date:      12/2/2011

A class implementing a simultaneous auction.
"""
from auctionBase import *

import numpy

class simultaneousAuction(auctionBase):
    """
    A class for simulating simultaneous one shot auctions.
    """
    def __init__(self, agentList = [], m = 5, name='simultaneousAuction'):
        
        
        self.setAgentList(agentList=agentList)
        
        super(simultaneousAuction,self).__init__(name)
        
        self.m = int(m)
        
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
        
    def addAgents(self, agentList = []):
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
        if targetAgent:
            self.agentList.remove(targetAgent)
            
    def runAuction(self,args={}):
        bids = []
        
        for agent in self.agentList:
            bids.append(agent.bid())
            
        bids = numpy.atleast_2d(bids)
        
        
            