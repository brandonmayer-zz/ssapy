from aucSim.agents.straightMU import *
from aucSim.agents.targetMU import *
from aucSim.agents.targetMUS import *
from aucSim.agents.targetPriceDist import *
from aucSim.agents.riskAware import *

from aucSim.pricePrediction.hist import *
from aucSim.pricePrediction.util import *

import argparse
import glob
from datetime import date
import matplotlib.pyplot as plot
import multiprocessing
import numpy
import time
import os

class worker(object):
    def __init__(self,**kwargs):
        numpy.testing.assert_('m' in kwargs, 
                              msg="Must Specify m in args.")
        numpy.testing.assert_('aType' in kwargs, 
                              msg="Must specify the type of participating agents.")
        numpy.testing.assert_('nAgents' in kwargs,
                              msg="Must specify the number of participating agents.")
        self.m       = kwargs['m']
        self.aType   = kwargs['aType']
        self.nAgents = kwargs['nAgents']
        
    def __call__(self,margDist = None):
        numpy.testing.assert_(margDist, 
                              'Must specify a marginal price distribution.')
        
        agentList = []
        if self.aType == 'straightMU8':
            agentList = [straightMU8(m = self.m) for i in xrange(self.nAgents)]
        elif self.aType == 'targetMU8':
            agentList = [targetMU8(m = self.m) for i in xrange(self.nAgents)]
        elif self.aType == 'targetMUS8':
            agentList = [targetMUS8(m = self.m) for i in xrange(self.nAgents)]
        else:
            print '-----ERROR-----'
            print 'UKNOWN AGENT TYPE {0}'.format(self.aType) 
            raise valueError
        
        #run the auction
        bids = [numpy.array(agent.bid(margDistPrediction = margDist)).astype('float') for agent in agentList]
        
        #return the winning bids
        return numpy.max(bids,0)  

def main():
    desc = 'Load margDistSCPP run a given number of games and compute the distance between original and resulting histogram'
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument( '--iPkl',   action = 'store', dest = 'iPkl',  required = True )
    parser.add_argument( '--oDir',   action = 'store', dest = 'oDir', required = True )
    parser.add_argument( '--aType',  action = 'store', dest = 'aType', required = True )
    
    parser.add_argument( '--nGames',  action = 'store', dest = 'nGames',  default = 1000000 )
    parser.add_argument( '--nAgents', action = 'store', dest = 'nAgents', default = 8 )
    parser.add_argument( '--nProc',   action = 'store', dest = 'nProc',   default = multiprocessing.cpu_count() - 1)
    parser.add_argument( '--verbose', action = 'store', dest = 'verbose', default = True, type = bool )
    parser.add_argument( '--serial',  action = 'store', dest = 'serial',  default = False, type = bool )
    parser.add_argument( '--plot',    action = 'store', dest = 'plot',    default = True, type = bool)
    
    args = parser.parse_args().__dict__
    
    if args['verbose']:
        table = []
        table.append(['iPkl', '{0}'.format(args['iPkl'])])
        table.append(['oDir', '{0}'.format(args['oDir'])])
        table.append(['aType', '{0}'.format(args['aType'])])
        table.append(['nGames', '{0}'.format(args['nGames'])])
        table.append(['nAgents', '{0}'.format(args['nAgents'])])
        table.append(['nProc', '{0}'.format(args['nProc'])])
        
        ppt(sys.stdout,table)
        del table
    
    #load the distribution
    margDist = margDistSCPP(args['iPkl'])
    m = margDist.m
    
    result = []
    if args['serial']:
        pass
    else:
        if args['verbose']:
            print 'Running Simulation'
        pool = multiprocessing.Pool(processes=args['nProc'])
        #instantiate the worker
        w = worker(aType   = args['aType'],
                   m       = m,
                   nAgents = args['nAgents'])
        
        result = numpy.atleast_2d(pool.map(w, itertools.repeat(margDist,args['nGames']))).astype(numpy.float)
        pool.close()
        pool.join()
        
    if args['verbose']:
        print 'Simulation Finished'
        print 'Histograming results.'
        
    histData  = []
    histCount = []
    #assuming all bin edges are the same
    binEdges = margDist.data[1][0]
    for m in xrange(result.shape[1]):
        histData.append(numpy.histogram(result[:,m],margDist.data[m][1],density=True))
        histCount.append(numpy.histogram(result[:,m],margDist.data[m][1],density=False))
        
    
    newDist = margDistSCPP(histData)
    
    kl = klDiv(margDist, newDist)   
    
    if args['verbose']:
        print 'KL Divergence = {0}'.format(kl)
        
    oFile = os.path.realpath(os.path.join(oDir,'klDiv.txt'))
    
    if args['verbose']:
        print 'Saving kl to {0}'.format(oFile)
        
    with open(ofile,'w') as f:
        f.write('{0}\n'.format(kl))
        
    if args['plot']:
        pFile = os.path.realpath(os.path.join(oDir,'evalDist.png'))
        
        if args['verbose']:
            print 'Plotting Eval Dist to {0}'.format(pFile)
        
        newDist.graphPdfToFile(pFile)

if __name__ == '__main__':
    main()