import numpy
import itertools
#from pricePrediction.dok_hist import dok_hist
from .pricePrediction.dokHist import dokHist

from ssapy.strategies import strategyDict

from ssapy.agents.marketSchedule import listRevenue as msListRevenue

from ssapy.agents.marketSchedule import \
    randomValueVector as msRandomValueVector
    
from ssapy.util import listBundles

#from ssapy.pricePrediction.dok_hist import dokDhist

def getStrategy(ss):
    strategy = strategyDict.get(ss)
    
    if strategy == None:
        raise ValueError("Unknown Strategy - {0}".format(strategy))
    
    return strategy
    



    

    

        


    
    

            

