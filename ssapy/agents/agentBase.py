'''
This is /aucSim/agents/agentBase.py

Author: Brandon A. Mayer
Date: 11/13/2011

The agent base class.
'''

class agentBase(object):
    """
    Base class for agents.
    
    Assigned each instantiated agent with a unique id
    """
    nextId = 0
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = 'Anonymous'
        
        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            self.id           = agentBase.nextId
            agentBase.nextId += 1

    def id(self):
        return self.id
    
    @staticmethod
    def type():
        return "agentBase"    