"""
This is /auctionSimulator/hw4/agents/pricePredicitonAgent.py

Author:        Brandon A. Mayer
Date:          11/26/2011

A base class for agents who participate in simultaneous auctions described by
Yoon & Wellman 2011 and use price prediction strategies.
"""
import sys

from simYW import *

from auctionSimulator.hw4.pricePrediction.pointSCPP import *
from auctionSimulator.hw4.pricePrediction.margDistSCPP import *

class pricePredictionAgent(simYW):
    """
    Base class for agents who use price prediciton in their strategy profiles.
    Defines the common member variable self.pricePrediction for both point and 
    distribution prediction schemes.
    
    This level of abstraction may be superfluous but I'll keep it for now.
    """
    def __init__(self,**kwargs):
        
        super(pricePredictionAgent,self).__init__(**kwargs)
        
        # defines the pricePrediciton member variable common to point and distribution
        # price prediction schemes
        if 'pricePrediction' in kwargs:
            self.loadOrSetPrediction(kwargs['pricePrediction'])
        else:
            self.pricePrediction = None
        
        
            
            
    def loadOrSetPrediction(self,pricePrediction):
        if isinstance(pricePrediction,basestring)\
             or isinstance(pricePrediction,file):
            
            self.loadPricePredictionPickle(self,pricePrediction)
            
        elif isinstance(pricePrediction,pointSCPP) or\
             isinstance(pricePrediction,margSCPP):
            self.setPricePrediction(pricePrediction)
            
        else:
            self.pricePrediction = None
        
    def loadPricePredictionPickle(self,f):
        """
        To load a pickled price prediction instance.
        INPUTS:
            f     either a string to a .pkl file 
                  or an opened pickle fileobject
        """
        if self.predictionType() == "pointSCPP":
            self.pricePrediction = pointSCPP()
            self.pricePrediction.loadPickle(f)
            
        elif self.predictionType() == "margDistSCPP":
            self.pricePrediction = margDistSCPP()
            self.pricePrediction.loadPickle(f)
        else:
            sys.stderr.write('----ERROR----\n')
            sys.stderr.write('pricePredictionAgent::loadPricePredictionPickle(f)\n')
            sys.stderr.write('Unknown self.predicitonType() = {0}'.format(self.predictionType()))
            raise AssertionError
        
    
    def setPricePrediction(self,pricePrediction):
        """
        To set the price prediction member variable but provide some level of type
        checking
        """
        if self.predictionType() == "pointSCPP":
            assert isinstance(pricePrediction,pointSCPP),\
            "----ERROR----\n" +\
            "{0}:setPricePrediction \n".format(self.type()) +\
            "self.predictionType() = {0} must match the pricePrediction type.".format(self.predictionType())
            self.pricePrediction = pricePrediction
            
        elif self.predictionType() == "margDistSCPP":
            assert isinstance(pricePrediction,margDistSCPP),\
            "----ERROR----\n" +\
            "{0}:setPricePrediction \n".format(self.type()) +\
            "self.predictionType() = {0} must match the pricePrediction type.".format(self.predictionType())
            self.pricePrediction = pricePrediction
        else:
            sys.stderr.write('----ERROR----\n')
            sys.stderr.write('pricePredictionAgent::setPricPrediction()\n')
            sys.stderr.write('Unknown self.predictionType() = {0}'.format(self.predictionType()))
            raise AssertionError
            
    @staticmethod
    def predictionType():
        sys.stderr.write('----ERROR----\n')
        sys.stderr.write('pricePredictionAgent::predictionType()\n')
        sys.stderr.write('cannot call method on abstract class')
        raise AssertionError
    
    @staticmethod
    def type():
        return "pricePredictionAgent"
          