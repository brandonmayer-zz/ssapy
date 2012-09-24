#!/usr/bin/env python

from ssapy.agents import agentFactory
from ssapy.pricePrediction.margDistSCPP import margDistSCPP
import numpy
import os
import argparse

def writeBidsFile(**kwargs):
    oDir = kwargs.get('oDir')
    agentType = kwargs.get('agentType')
    ppFile = kwargs.get('ppFile')
    bidsFile = kwargs.get('bidsFile')
    
    bidsFile = os.path.realpath(bidsFile)
    ppFile = os.path.realpath(ppFile)
    oDir = os.path.realpath(oDir)
    if not os.path.exists(oDir):
        os.makedirs(oDir)
    
    data = numpy.loadtxt(bidsFile)
    
#    ppCounts = numpy.loadtxt(ppFile,delimiter=",",dtype=numpy.float)
#    
#    prob = []
#    for counts in ppCounts:
#        prob.append(counts/sum(counts))
#            
#    expectedPriceVector = []
#    
#    for p in prob:
#        expectedPriceVector.append(numpy.dot(p,numpy.arange(0,51)))
#            
#    expectedPriceVector = numpy.atleast_1d(expectedPriceVector)
    
    margDist = margDistSCPP()
    margDist.loadWellmanCsv(ppFile)
    expectedPriceVector = margDist.expectedPrices(method='average')
    
    sampleExpectedVector = margDist.sample(n_samples=1000)
    sampleExpectedVector = numpy.mean(sampleExpectedVector,0)
    
    agent = agentFactory.agentFactory(agentType = agentType, m = 5, minPrice = 0, maxPrice = 50)
        
    output = numpy.zeros(data.shape)
    for row, sim in enumerate(data):
        output[row,0:6] = sim[0:6]
        agent.l = int(sim[0])
        agent.v = sim[1:6]
        
        bidVector = agent.bid(pricePrediction = expectedPriceVector)
        print 'Mayer Bid  = {0}'.format(bidVector)
        print 'Welman Bid = {0}'.format(sim[6:])
        output[row,6:] = bidVector
        
    oFile = os.path.join(oDir, '{0}-bids.txt'.format(agentType))
    numpy.savetxt(oFile, output)
    
    

def main():
    desc = 'Given Price Prediction strategy, search for self-confirming price prediction using marginal bayesian method'
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('--oDir', action = 'store', dest = 'oDir', required = True,
                        help = "Must provide output directory")
    
    parser.add_argument('--bidsFile', action = 'store', dest = 'bidsFile', required = True,
                        help = "Wellmans [agent-type]-bids.txt file to use as ground truth")
    
    parser.add_argument('--ppFile', action = 'store', dest = 'ppFile', required = True,
                        help = "Wellmans price prediction file [agentParameters].csv to use a price prediction")
    
    parser.add_argument('--agentType', action = 'store', dest = 'agentType', required = True,
                        help = "Mayer's equivalent agent type.")

    args = parser.parse_args().__dict__
    
    writeBidsFile(**args)
    
if __name__ == "__main__":
    main()
