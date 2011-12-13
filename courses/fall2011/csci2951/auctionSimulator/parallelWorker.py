from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.agents.straightMU import *
from auctionSimulator.hw4.agents.averageMU import *
from auctionSimulator.hw4.agents.targetMU import *
from auctionSimulator.hw4.agents.targetMUS import *
from auctionSimulator.hw4.agents.baselineBidder import *
from auctionSimulator.hw4.agents.bidEvaluator import *

from auctionSimulator.hw4.auctions.simultaneousAuction import *

import numpy
import multiprocessing

class parallelWorkerBase(object):
    def __init__(self, **kwargs):
        pass
    
    def __call__(self,*args):
        pass

class parallelSimAuctionSymmetricVL(parallelWorkerBase):
    """
    NOTE:
        THIS WORKER ASSUMES THAT ALL AGENTS HAVE THE SAME
        VALUATION AND TARGET NUMBER OF GOODS!!!!
    """
    def __init__(self, **kwargs):
        
        numpy.testing.assert_('margDistPrediction' in kwargs,
                              msg="Must specify a margianl price prediction distribution.")
        
        numpy.testing.assert_(isinstance(kwargs['margDistPrediction'],margDistSCPP),
                              msg="margDistPrediction must be an instance of margDistSCPP")
        
        numpy.testing.assert_('agentList' in kwargs,
                              msg="Must specify a list of agents.")
        
        if isinstance(kwargs['agentList'],list):
            [numpy.testing.assert_(isinstance(agent,basestring)) for agent in kwargs['agentList']]
        
        self.agentTypeList = kwargs['agentList']
        
        self.nGames = kwargs.get('nGames',100)
        
        self.m      = kwargs.get('m',5)
        
        self.margDistPrediction = kwargs['margDistPrediction']
        
        self.A = kwargs.get('A')
    
        self.vmin = kwargs.get('vmin',0)
        
        self.vmax = kwargs.get('vmax',50)
        
    def agentsFromType(self,**kwargs):
        try:
            agentTypeList = kwargs['agentTypeList']
        except:
            raise KeyError('Must specify agentTypeList')
        
        #will be set to none if not specified
        margDistPrediction = kwargs.get('margDistPrediction',self.margDistPrediction)
        m = kwargs.get('m',self.m)
        
        agentList = []
        for i, agentType in enumerate(agentTypeList):
            if agentTypeList[i] == 'riskAwareTP8':
                
                A = kwargs.get('A',self.A)
                if A == None:
                    raise KeyError('Must Specify A valu of A if a riskAware Agent is specified.')
                    
                agentList.append(riskAwareTP8( m                       = m,
                                               margDistPricePrediction = margDistPrediction,
                                               A                       = A) )
            elif agentTypeList[i] == 'riskAwareTMUS8':
                
                A = kwargs.get('A',self.A)
                if A == None:
                    raise KeyError('Must Specify A valu of A if a riskAware Agent is specified.')
                
                agentList.append(riskAwareTMUS8( m                       = m,
                                                 margDistPricePrediction = margDistPrediction,
                                                 A                       = A))
            elif agentTypeList[i] == 'targetMUS8':
                agentList.append(targetMUS8(m                       = m,
                                                 margDistPricePrediction = margDistPrediction))
            elif agentTypeList[i] == 'targetMU8':
                agentList.append(targetMU8(m                       = m,
                                                 margDistPricePrediction = margDistPrediction))
            elif agentTypeList[i] == 'straightMU8':
                agentList.append(straightMU8(m                       = m,
                                                 margDistPricePrediction = margDistPrediction))
            elif agentTypeList[i] == 'averageMU':
                agentList.append(averageMU(m                       = m,
                                           margDistPricePrediction = margDistPrediction))
            elif agentTypeList[i] == 'bidEvaluatorSMU8':
                agentList.append(bidEvaluatorSMU8(m                       = m,
                                                  margDistPricePrediction = margDistPrediction))
            elif agentTypeList[i] == 'bidEvaluatorTMUS8':
                agentList.append(bidEvaluatorTMUS8(m                       = m,
                                                   margDistPricePrediction = margDistPrediction))
            else:
                raise ValueError('Unknown Agent Type {0}'.format(agentTypeList[i]))
            
        return agentList
        
            
        
    def __call__(self,*args):
        
        agentList = self.agentsFromType(agentTypeList      = self.agentTypeList,
                                        A                  = self.A,
                                        m                  = self.m,
                                        margDistPrediction = self.margDistPrediction)
#        for i in xrange(len(self.agentTypeList)):
#            
#            if self.agentTypeList[i] == 'riskAwareTP8':
#                agentList.append(riskAwareTP8( m                       = self.m,
#                                               margDistPricePrediction = self.margDistPrediction,
#                                               A                       = self.A))
#            elif self.agentTypeList[i] == 'riskAwareTMUS8':
#                agentList.append(riskAwareTMUS8(m                       = self.m, 
#                                                margDistPricePrediction = self.margDistPrediction,
#                                                A                       = self.A))
#            elif self.agentTypeList[i] == 'targetMUS8':
#                agentList.append(targetMUS8(m                       = self.m, 
#                                            margDistPricePrediction = self.margDistPrediction))
#            elif self.agentTypeList[i] == 'targetMU8':
#                agentList.append(targetMU8(m                       = self.m, 
#                                           margDistPricePrediction = self.margDistPrediction))
#            elif self.agentTypeList[i] == 'straightMU8':
#                agentList.append(straightMU8(m                       = self.m,
#                                             margDistPricePrediction = self.margDistPrediction))
#            elif self.agentTypeList[i] == 'averageMU':
#                agentList.append(averageMU(m                       = self.m,
#                                           margDistPricePrediction = self.margDistPrediction))
#            elif self.agentTypeList[i] == 'bidEvaluatorSMU8':
#                agentList.append(bidEvaluatorSMU8(m                       = self.m,
#                                                  margDistPricePrediction = self.margDistPrediction))
#            elif self.agentTypeList[i] == 'bidEvaluatorTMUS8':
#                agentList.append(bidEvaluatorTMUS8(m                       = self.m,
#                                                   margDistPricePrediction = self.margDistPrediction))
#            else:
#                raise ValueError('Unknown Agent Type {0}'.format(self.agentTypeList[i]))
        
        agentSurplus = []
        
        for g in xrange(0,self.nGames):
                        
            v = numpy.random.random_integers(low = self.vmin, high = self.vmax, size= self.m)
            
            v.sort()
            
            v = v[::-1]
            
            l = numpy.random.random_integers(low = 1, high = self.m)
            
            for agent in agentList:
                agent.v = v
                agent.l = l
            
            auction = simultaneousAuction(agentList = agentList)
            
            auction.runAuction()
            
            auction.notifyAgents()
            
            agentSurplus.append( auction.agentSurplus() )
            
        return numpy.atleast_2d(agentSurplus).astype(numpy.float)
    
    
def runParallelJob(**kwargs):
    
    pw = kwargs['parallelWorker']
    
    numpy.testing.assert_(isinstance(pw,parallelWorkerBase))
    
    pool = multiprocessing.Pool(processes = kwargs.get('NUMP_PROC', multiprocessing.cpu_count() - 1))
    
    result = numpy.atleast_2d(pool.map(pw, xrange(0,NUM_PROC))).astype(kwargs.get('resultType',numpy.float))
    
    return numpy.reshape( result,(result.shape[0]*result.shape[1],result.shape[2]) )    
            
            