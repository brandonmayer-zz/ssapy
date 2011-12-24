import os
import glob
import aucSim

class conf(object):
    def __init__(self,**kwargs):
        self.auctionSimulatorDir = os.path.dirname(aucSim.__file__)
#        self.auctionTestsDir = os.path.dirname(auctionTests.__file__)
        
        self.pricePredictionDir = os.path.join(self.auctionSimulatorDir,'hw4','pricePrediction')
        self.margDistPredictionDir = os.path.join(self.pricePredictionDir,'margDistPredictions')
        self.pointPricePredictionDir = os.path.join(self.pricePredictionDir,'pointPricePredictions')
        
        self.agentDir = os.path.join(self.auctionSimulatorDir,'hw4','agents')
        self.auctionDir = os.path.join(self.auctionSimulatorDir,'hw4','auctions')
        
        self.margDistPklFiles = dict()
        
        for file in glob.glob( os.path.join(self.margDistPredictionDir,'*.pkl') ):
            self.margDistPklFiles[os.path.basename(file)] = file
            
        self.pointPklFiles = dict()
        for file in glob.glob(os.path.join(self.pointPricePredictionDir,'*.pkl')):
            self.pointPklFiles[os.path.basename(file)] = file
            
            
        #set up output experiment directory given the computer i'm using
        self.usr = kwargs.get('usr', 'desktop')
        if self.usr == 'desktop':
            self.expDir = 'F:\\courses\\fall2011\\csci2951\\hw4'
#            
        elif self.usr == 'laptop':
            self.expDir = 'C:\\coursesFall2011\\csci2951\\exp'        

config = conf()
