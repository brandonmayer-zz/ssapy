from ssapy.agents.straightMU import straightMV, straightMU, straightMU8, straightMU64, straightMU256
from ssapy.agents.targetMU import targetMV, targetMU, targetMU8
from ssapy.agents.targetMUS import targetMVS, targetMUS, targetMUS8, targetMUS64
from ssapy.agents.targetPrice import targetPrice
from ssapy.agents.targetPriceDist import targetPriceDist, targetPrice8, targetPrice64, targetPrice256
from ssapy.agents.riskAware import riskEvaluator8, riskEvaluator64, riskAwareTMUS256

def margAgentFactory(**kwargs):
    agentType = kwargs.get('agentType')
    m         = kwargs.get('m',5)

    agent = None
    
    if agentType == "straightMV":
        agent = straightMV(m=m)
    elif agentType == "straightMU":
        agent = straightMU(m=m)
    elif agentType == "straightMU8":
        agent = straightMU8(m=m)
    elif agentType == "straightMU64":
        agent = straightMU64(m=m)
    elif agentType == "straightMU256":
        agent = straightMU256(m=m)
    elif agentType == "targetMV":
        agent = targetMV(m = m)
    elif agentType == "targetMU":
        agent = targetMU(m = m)
    elif agentType == "targetMU8":
        agent = targetMU8(m=m)
    elif agentType == "targetMVS":
        agent = targetMVS(m=m)
    elif agentType == "targetMUS":
        agent = targetMUS(m=m)
    elif agentType == "targetMUS8":
        agent = targetMUS8(m=m)
    elif agentType == "targetMUS64":
        agent = targetMUS64(m=m)
    elif agentType == "targetPrice":
        agent = targetPrice(m=m)
    elif agentType == "targetPriceDist":
        agent = targetPriceDist(m=m)
    elif agentType == "targetPrice8":
        agent = targetPrice8(m=m)
    elif agentType == "targetPrice64":
        agent = targetPrice64(m=m)
    elif agentType == "targetPrice256":
        agent = targetPrice256(m=m)
    elif agentType == "riskEvaluator8":
        agent = riskEvaluator8(m=m)
    elif agentType == "riskEvaluator64":
        agent = riskEvaluator64(m=m)
    elif agenttype == "riskEvaluator256":
        agent = riskEvaluator256(m=m)
        
    return agent
    
    

