"""
this is /auctionSimulator/hw4/agents/auctionBase.py

Author:    Brandon A. Mayer
Date:      11/23/2011
"""

class auctionBase(object):
    nextId = 0
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Anonymous')
        self.id = auctionBase.nextId
        auctionBase.nextId +=1
        
    def id(self):
        return self.id
    
    @staticmethod
    def type():
        return auctionBase
        