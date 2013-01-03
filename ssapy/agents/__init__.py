'''
This is /ssapy/agents/__init__.py

Author: Brandon A. Mayer
Date: 11/13/2011

The agent base class.

Modifications:
    Brandon A. Mayer - 1/1/2013 moved agentBase here.
'''
from ssapy.util import surplus

class agentBase(object):
    """
    Base class for agents.
    
    Assigned each instantiated agent with a unique id
    """
    nextId = 0
    def __init__(self, **kwargs):
        
        self.name = kwargs.get('Name','Anonymous')
        
        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            self.id           = agentBase.nextId
            agentBase.nextId += 1
            
        self.bundleWon = None
        
        self.finalPrices = None
            
    def id(self):
        return self.id
    
    def finalSurplus(self, **kwargs):
        if self.bundleWon == None:
            raise KeyError("Agent {0} : {1} self.bundleWon = None".\
                           format(self.id, self.name))
                           
        if self.finalPrices == None:
            raise KeyError("Agent {0} : {1} self.finalPrices = None".\
                           format(self.id,self.name))
            
        val = kwargs.get('valuation')
        
        if val == None:
            raise KeyError("Must Specify Valuation for won bundle.")
            
        return surplus( self.bundleWon,
                        val, self.finalPrices)
    
    @staticmethod
    def type():
        return "agentBase"  
