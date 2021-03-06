#from aucSim.agents import *
from ssapy.agents.riskAware import riskAwareTMUS64, riskEvaluator8, riskEvaluator64, riskAwareTMUS256
from ssapy.agents.targetMU import targetMUS8, targetMU8
from ssapy.agents.averageMU import averageMU
from ssapy.agents.bidEvaluator import bidEvaluatorSMU8, bidEvaluatorSMU64, bidEvaluatorTMUS8, bidEvaluatorRaTMUS8
 
#from aucSim.simultaneousAuction import *
from ssapy.auctions.simultaneousAuction import simultaneousAuction 

import numpy
import multiprocessing

class parallelWorkerBase(object):
    def __init__(self, **kwargs):
        
        self.agentTypeList      = kwargs.get('agentList')
        self.nGames             = kwargs.get('nGames',100)
        self.m                  = kwargs.get('m',5)
        self.margDistPrediction = kwargs.get('margDistPrediction')        
        self.A                  = kwargs.get('A')    
        self.vmin               = kwargs.get('vmin',0)
        self.vmax               = kwargs.get('vmax',50)
        
        numpy.testing.assert_('margDistPrediction' in kwargs,
                              msg="Must specify a margianl price prediction distribution.")
        
        numpy.testing.assert_(isinstance(kwargs['margDistPrediction'],margDistSCPP),
                              msg="margDistPrediction must be an instance of margDistSCPP")
        
        if isinstance(self.agentTypeList,list):
            [numpy.testing.assert_(isinstance(agent,basestring)) for agent in kwargs['agentList']]
    
    def __call__(self,*args, **kwargs):
        raise AssertionError('Cannot Call a parallelWorkerBase')
    
    def agentsFromType(self,**kwargs):
        """
        Construct agents from a list of strings. An agent factory.
        """
        agentTypeList = kwargs.get('agentTypeList',self.agentTypeList)
            
        #will be set to none if not specified
        margDistPrediction = kwargs.get('margDistPrediction',self.margDistPrediction)
        
        m = kwargs.get('m',margDistPrediction.m)
        
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
            elif agentTypeList[i] == 'riskAwareTMUS64':
                
                A = kwargs.get('A',self.A)
                if A == None:
                    raise KeyError('Must Specify A valu of A if a riskAware Agent is specified.')
                    
                agentList.append(riskAwareTMUS64( m                       = m,
                                                  margDistPricePrediction = margDistPrediction,
                                                  A                       = A) )
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
            elif agentTypeList[i] == 'bidEvaluatorSMU64':
                agentList.append(bidEvaluatorSMU64(m                       = m,
                                                  margDistPricePrediction = margDistPrediction))
            elif agentTypeList[i] == 'bidEvaluatorTMUS8':
                agentList.append(bidEvaluatorTMUS8(m                       = m,
                                                   margDistPricePrediction = margDistPrediction))
            elif agentTypeList[i] == 'bidEvaluatorRaTMUS8':
                A = kwargs.get('A',self.A)
                if A == None:
                    raise KeyError('Must Specify A valu of A if a riskAware Agent is specified.')
                agentList.append(bidEvaluatorRaTMUS8(m                       = m,
                                                     margDistPricePrediction = margDistPrediction,
                                                     A                       = A))
            elif agentTypeList[i] == 'riskEvaluator8':
                A = kwargs.get('A',self.A)
                if A == None:
                    raise KeyError('Must Specify A valu of A if a riskAware Agent is specified.')
                agentList.append(riskEvaluator8(m                       = m,
                                                margDistPricePrediction = margDistPrediction,
                                                A                       = A))
                
            elif agentTypeList[i] == 'riskEvaluator64':
                A = kwargs.get('A',self.A)
                if A == None:
                    raise KeyError('Must Specify A valu of A if a riskAware Agent is specified.')
                agentList.append(riskEvaluator64(m                       = m,
                                                 margDistPricePrediction = margDistPrediction,
                                                 A                       = A))
                
            elif agentTypeList[i] == 'riskEvaluator256':
                A = kwargs.get('A',self.A)
                if A == None:
                    raise KeyError('Must Specify A valu of A if a riskAware Agent is specified.')
                agentList.append(riskEvaluator256(m                       = m,
                                                  margDistPricePrediction = margDistPrediction,
                                                  A                       = A))
            else:
                raise ValueError('Unknown Agent Type {0}'.format(agentTypeList[i]))
            
        return agentList

class pwEqVl(parallelWorkerBase):
    """
    NOTE:
        THIS WORKER ASSUMES THAT ALL AGENTS HAVE THE SAME
        VALUATION AND TARGET NUMBER OF GOODS!!!!
    """    
    def __call__(self, *args , **kwargs):
        
        agentList = self.agentsFromType(agentTypeList      = self.agentTypeList,
                                        A                  = self.A,
                                        m                  = self.m,
                                        margDistPrediction = self.margDistPrediction)
               
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
    
    
class pwEqNgames(parallelWorkerBase):
    """
    In every game, every agent draws a valuation function from
    the same underlying distribution (symmetric game).
    """
    def __call__(self, *args, **kwargs):
        
        agentList = self.agentsFromType(agentTypeList      = self.agentTypeList,
                                        A                  = self.A,
                                        m                  = self.m,
                                        margDistPrediction = self.margDistPrediction)
        
        agentSurplus = []
        
        for g in xrange(self.nGames):
            
            # all agents draw new valuation function
            for agent in agentList:
                agent.randomValuation(vmin = self.vmin,
                                      vmax = self.vmax,
                                      m     = self.m)
                
            auction = simultaneousAuction(agentList = agentList)
            
            auction.runAuction()
            
            auction.notifyAgents()
            
            agentSurplus.append( auction.agentSurplus() )
            
        return numpy.atleast_2d(agentSurplus).astype(numpy.float)  
    
class pwVarNgames(parallelWorkerBase):
    """
    Same as parallelSimAuctionSymmetric but takes to each call
    a single argument that indicates how many iterations to run 
    per loop
    """
    def __call__(self, *args, **kwargs):
        
        nGames = self.nGames
        if args:
            nGames = args[0]
            
        agentList = self.agentsFromType(agentTypeList      = self.agentTypeList,
                                        A                  = self.A,
                                        m                  = self.m,
                                        margDistPrediction = self.margDistPrediction)
                                        
        agentSurplus = []
        
        for g in xrange(nGames):
            
            # all agents draw new valuation function
            for agent in agentList:
                agent.randomValuation(vmin = self.vmin,
                                      vmax = self.vmax,
                                      m     = self.m)
                auction = simultaneousAuction(agentList = agentList)
            
            auction.runAuction()
            
            auction.notifyAgents()
            
            agentSurplus.append( auction.agentSurplus() )
            
        return numpy.atleast_2d(agentSurplus).astype(numpy.float) 
        
        
    
def runParallelJob(**kwargs):
    try:
        pw = kwargs['parallelWorker']
    except KeyError:
        raise KeyError('Must specify a parallel worker functor.')
    
    NUM_PROC = kwargs.get('NUM_PROC', multiprocessing.cpu_count() - 1)
    
    numpy.testing.assert_(isinstance(pw,parallelWorkerBase))
    
    pool = multiprocessing.Pool(processes = NUM_PROC)

    if isinstance(pw,pwEqVl) or isinstance(pw,pwEqNgames):
        result = numpy.atleast_2d(pool.map(pw, xrange(0,NUM_PROC))).astype(kwargs.get('resultType',numpy.float))
    if isinstance(pw,pwVarNgames):
        # a list of number of games
        try:
            nGameList = kwargs['nGameList']
        except KeyError:
            raise KeyError('Must specify the number of games each auction will run with nGameList parameter')
        
        result = numpy.atleast_2d(pool.map(pw, nGameList)).astype(kwargs.get('resultType',numpy.float)) 
        
    return numpy.reshape( result,(result.shape[0]*result.shape[1],result.shape[2]) )    
            
            