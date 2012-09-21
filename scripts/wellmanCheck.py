#!/usr/env/ python

from ssapy.agents import agentFactory
import numpy
import os

def readBidsFile(filename):
    data = numpy.loadtxt(filename)
    
    return data

def computeExpectedValues(ppCounts):
    pass
    

def writeBidsFile(oDir, agentType, bidsFile, ppFile):
    
    bidsFile = os.path.realpath(bidsFile)
    ppFile = os.path.realpath(ppFile)
    oDir = os.path.realpath(oDir)
    if not os.path.exists(oDir):
        os.makedirs(oDir)
    
    data = numpy.loadtxt(bidsFile)
    
    ppCounts = numpy.loadtxt(ppFile,delimiter=",")
    
    prob = []
    for counts in ppCounts:
        prob.append(counts/sum(counts))
        
    expectedPriceVector = []
    for p in prob:
        expectedPriceVector.append(numpy.dot(p,numpy.arange(0,51)))
        
        
    expectedPriceVector = numpy.atleast_1d(expectedPriceVector)
    
    agent = agentFactory.agentFactory(agentType = agentType, m = 5, minPrice = 0, maxPrice = 50)
    
    output = numpy.zeros(data.shape)
    for row, sim in enumerate(data):
        output[row,0:6] = sim[0:6]
        agent.l = sim[0]
        agent.v = sim[1:6]
        output[7:] = agent.bid(pointPricePrediction = expectedPriceVector)
        
    oFile = os.path.join(oDir, '{0}-bids.txt'.format(agentType))
    numpy.savetxt(oFile, output)
    
    

#def main():
#    desc = 'Given Price Prediction strategy, search for self-confirming price prediction using marginal bayesian method'
#    parser = argparse.ArgumentParser(description=desc)
    
#    parser.add_argument('--agentType', action = 'store', dest = 'oDir')
    
if __name__ == "__main__":
    bidsFile = "/gpfs/main/research/tac/joint-results/wellmanSimulations/javaResults/AvgMU-bids.txt"

    ppFile = "/gpfs/main/research/tac/joint-results/wellmanSimulations/javaResults/OSSCDP_AverageMU64_HB_N5M5V50.csv"
    
    oDir = "/gpfs/main/research/tac/joint-results/wellmanSimulations/pythonResults"
    
    agentType = "averageMU"
    
    writeBidsFile(oDir, agentType, bidsFile, ppFile)