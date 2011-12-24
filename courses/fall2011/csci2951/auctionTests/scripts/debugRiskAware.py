from auctionSimulator.hw4.auctions.simultaneousAuction import *
from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.agents.straightMU import *
from auctionSimulator.hw4.agents.targetPriceDist import *

import numpy

def main():
    
    margDistPkl = "C:\\bmProjects\\courses\\fall2011\\csci2951\\" +\
                  "auctionSimulator\\hw4\\pricePrediction\\margDistPredictions\\" +\
                  "distPricePrediction_straightMU_10000_2011_12_4_1323040769.pkl"
    
    margDistPrediction=margDistSCPP()
    
    margDistPrediction.loadPickle(margDistPkl)
    agentList = []
    
    riskAware1 = riskAware(margDistPricePrediction = margDistPrediction,
                           A                       = 3)
    
    
    riskAware1.printSummary()    

if __name__ == "__main__":
    main()