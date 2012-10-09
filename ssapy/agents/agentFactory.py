from ssapy.agents.straightMU import straightMV, straightMU, straightMU8, straightMU64, straightMU256
from ssapy.agents.targetMU import targetMV, targetMU, targetMU8, targetMU64, targetMU256
from ssapy.agents.targetMUS import targetMVS, targetMUS, targetMUS8, targetMUS64, targetMUS256
from ssapy.agents.targetPrice import targetPrice
from ssapy.agents.targetPriceDist import targetPriceDist, targetPrice8, targetPrice64, targetPrice256
from ssapy.agents.riskAware import riskEvaluator8, riskEvaluator64, riskAwareTMUS256
from ssapy.agents.averageMU import averageMU, averageMU8, averageMU64, averageMU256
from ssapy.agents.localBid import localBid
from ssapy.agents.condLocalBid import condLocalBid
from ssapy.agents.margLocalBid import margLocalBid

def agentFactory(**kwargs):
    agentType = kwargs.get('agentType')
    m         = kwargs.get('m',5)
    vmin  = kwargs.get('vmin',0)
    vmax  = kwargs.get('vmax',50)

    if agentType == None:
        raise ValueError("Must specify Agent Type")
    
    if agentType == "straightMV":
        agent = straightMV(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "straightMU":
        agent = straightMU(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "straightMU8":
        agent = straightMU8(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "straightMU64":
        agent = straightMU64(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "straightMU256":
        agent = straightMU256(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetMV":
        agent = targetMV(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetMU":
        agent = targetMU(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetMU8":
        agent = targetMU8(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetMU64":
        agent = targetMU64(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetMU256":
        agent = targetMU256(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetMVS":
        agent = targetMVS(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetMUS":
        agent = targetMUS(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetMUS8":
        agent = targetMUS8(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetMUS64":
        agent = targetMUS64(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetMUS256":
        agent = targetMUS256(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetPrice":
        agent = targetPrice(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetPriceDist":
        agent = targetPriceDist(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetPrice8":
        agent = targetPrice8(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetPrice64":
        agent = targetPrice64(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "targetPrice256":
        agent = targetPrice256(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "riskEvaluator8":
        agent = riskEvaluator8(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "riskEvaluator64":
        agent = riskEvaluator64(m = m, vmin = vmin, vmax = vmax)
#    elif agentType == "riskEvaluator256":
#        agent = riskEvaluator256(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "averageMU":
        agent = averageMU(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "averageMU8":
        agent = averageMU8(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "averageMU64":
        agent = averageMU64(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "averageMU256":
        agent = averageMU256(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "localBid":
        agent = localBid(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "condLocalBid":
        agent = condLocalBid(m = m, vmin = vmin, vmax = vmax)
    elif agentType == "margLocalBid":
        agent = margLocalBid(m = m,vmin = vmin, vmax = vmax)
    else:
        raise ValueError("{0} not defined in agentFactory".format(agentType))

    return agent