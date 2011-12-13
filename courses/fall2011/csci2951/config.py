import os
import glob

class conf(object):
    def __init__(self,**kwargs):
        self.cwd = os.getcwd()
        self.auctionSimulatorDir = os.path.join(self.cwd,'auctionSimulator')
        self.auctionTestsDir = os.path.join(self.cwd,'auctionTests')
        
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

config = conf()
pass