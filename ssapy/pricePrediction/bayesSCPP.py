from ssapy.pricePrediction.util import ksStat, klDiv
from ssapy.pricePrediction.hist import hist

import numpy
import matplotlib.pyplot as plt
import time
import os
import glob
import json
import shutil

def bayesSCPP(**kwargs):
    oDir      = kwargs.get('oDir')
    agentType = kwargs.get('agentType')
    nAgents   = kwargs.get('nAgents',8)
    m         = kwargs.get('m',5)
    minPrice  = kwargs.get('minPrice',0)
    maxPrice  = kwargs.get('maxPrice',50)
    delta     = kwargs.get('delta', 1)
    maxSim    = kwargs.get('maxSim', 1000)
    nGames    = kwargs.get('nGames', 100)
    parallel  = kwargs.get('parallel', False)
    tol       = kwargs.get('tol',0.001)
    log       = kwargs.get('log', True)
    
    if not oDir:
        str = "-----ERROR-----\n" +\
              "In bayesSCPP(...)\n" +\
              "Must Provide output directory\n"
        raise ValueError(str)
    
    if not os.path.exists(oDir):
        os.makedirs(oDir)
    if log:
        logFile = os.path.join(oDir,'bayesSCPP_{0}.txt'.format(agentType))
        if os.path.exists(logFile):
            os.remove(logFile)
            
        with open(logFile,'a') as f:
            f.write("oDir      = {0}".format(oDir))
            f.write("agentType = {0}".format(agentType))
            f.write("nAgents   = {0}".format(nAgents))
            f.write("tol       = {0}".format(tol))
            f.write("m         = {0}".format(m))
            f.write("minPrice  = {0}".format(minPrice))
            f.write("maxPrice  = {0}".format(maxPrice))
            f.write("delta     = {0}".format(delta))
            f.write("maxSim    = {0}".format(maxSim))
            f.write("nGames    = {0}".format(nGames))
            f.write("parallel  = {0}".format(parallel))
        
    
    
    currHist = hist()
    oFile = os.path.join(outDir,'bayesSCPP_itr_{0}.png'.format(0))
    title='bayesSCPP, {0}, Initial Distribution'.format(agentType)
    currHist.bayesMargDistSCPP().graphPdfToFile(fname = oFile,
                                                title=title)
    