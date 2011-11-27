"""
This is /auctionSimulator/hw4/agents/pointPredictionAgent.py

Author:        Brandon A. Mayer
Date:          11/27/2011

A base class for agents who utilize a distribution price prediction.
"""
from pricePredicitonAgent import *
from auctionSimulator.hw4.pricePrediction.margDistSCPP import *

class margDistPredictionAgent(pricePredictionAgent):
    def __init__(self,
                 m = 5,
                 v = None,
                 l = None,
                 vmin = 0,
                 vmax = 50,
                 pricePrediction = None,
                 name = "Anonymous"):
        super(margDistPredictionAgent,self).__init__(m=m,v=v,l=l,vmin=vmin,vmax=vmax,name=name)
        
        if isinstance(pricePrediction,basestring)\
             or isinstance(pricePrediction,file):
            self.loadPricePredictionPickle(self,pricePrediction)
        elif isinstance(pricePrediciton,pointSCPP):
            self.setPricePrediction(pricePrediction)
            
    @staticmethod
    def predictionType():
        return "margDistSCPP"
    
    @staticmethod
    def type():
        return "margDistPredictionAgent"