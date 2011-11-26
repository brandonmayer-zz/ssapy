import auctionSimulator.hw4.agents as hw4_agents
from auctionSimulator.hw4.pricePrediction.marginalDistributionSCPP import * 
import itertools
import numpy
import multiprocessing

import os
  
if __name__ == '__main__':
    
    m = 5
    
    hist = numpy.random.random_integers(1,10,50)
    binEdges = numpy.arange(1,51)
    myDist = marginalDistributionSCPP((hist,binEdges))
    
    pass
    
    