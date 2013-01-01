import numpy
import itertools
from pricePrediction.dok_hist import dok_hist

from ssapy.strategies import strategyDict

from ssapy.pricePrediction.dok_hist import dok_hist

def getStrategy(ss):
    strategy = strategyDict.get(ss)
    
    if strategy == None:
        raise ValueError("Unknown Strategy - {0}".format(strategy))
    
    return strategy
    



    

    

        


    
    

            

