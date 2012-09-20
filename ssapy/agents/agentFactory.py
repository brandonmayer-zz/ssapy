from ssapy.agents.straightMU import straightMV, straightMU, straightMU8, straightMU64, straightMU256
from ssapy.agents.targetMU import targetMV, targetMU, targetMU8
from ssapy.agents.targetMUS import targetMVS, targetMUS, targetMUS8, targetMUS64
from ssapy.agents.targetPrice import targetPrice
from ssapy.agents.targetPriceDist import targetPriceDist, targetPrice8, targetPrice64, targetPrice256
from ssapy.agents.riskAware import riskEvaluator8, riskEvaluator64, riskAwareTMUS256
from ssapy.agents.averageMU import averageMU, averageMU8, averageMU64, averageMU256

def agentFactory(**kwargs):
    agentType = kwargs.get('agentType')
    m         = kwargs.get('m',5)
    minPrice  = kwargs.get('vmin',0)
    maxPrice  = kwargs.get('vmax',50)

    agent = None
    
    if agentType == "straightMV":
        agent = straightMV(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "straightMU":
        agent = straightMU(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "straightMU8":
        agent = straightMU8(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "straightMU64":
        agent = straightMU64(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "straightMU256":
        agent = straightMU256(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "targetMV":
        agent = targetMV(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "targetMU":
        agent = targetMU(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "targetMU8":
        agent = targetMU8(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "targetMVS":
        agent = targetMVS(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "targetMUS":
        agent = targetMUS(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "targetMUS8":
        agent = targetMUS8(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "targetMUS64":
        agent = targetMUS64(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "targetPrice":
        agent = targetPrice(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "targetPriceDist":
        agent = targetPriceDist(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "targetPrice8":
        agent = targetPrice8(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "targetPrice64":
        agent = targetPrice64(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "targetPrice256":
        agent = targetPrice256(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "riskEvaluator8":
        agent = riskEvaluator8(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "riskEvaluator64":
        agent = riskEvaluator64(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "riskEvaluator256":
        agent = riskEvaluator256(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "averageMU8":
        agent = averageMU8(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "averageMU64":
        agent = averageMU64(m = m, vmin = minPrice, vmax = maxPrice)
    elif agentType == "averageMU256":
        agent = averageMU256(m = m, vmin = minPrice, vmax = maxPrice)
        
    return agent
    
    

