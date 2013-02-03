from .marketSchedule.baselineBidder import baselineBidder
from .marketSchedule.straightMV import straightMV
from .marketSchedule.targetPrice import targetPrice8, targetPrice64, targetPrice256
from .marketSchedule import straightMU as msStraightMU
from .marketSchedule import straightMV as msStraightMV
from .marketSchedule import targetPrice as msTargetPrice
from .marketSchedule.condMVLocal import condMVLocal as msCondMVLocal
from .marketSchedule.jointLocal import jointLocal



def agentFactory(**kwargs):
    agentType = kwargs.get('agentType')
    if agentType == None:
        raise ValueError("Must provide agentType (string).")
    elif agentType == "msStraightMV":
        return msStraightMV.straightMV(**kwargs)
    elif agentType == "msStraightMUa":
        return msStraightMU.straightMUa(**kwargs)
    elif agentType == "msStraightMU8":
        return msStraightMU.straightMU8(**kwargs)
    elif agentType == "msStraightMU64":
        return msStraightMU.straightMU64(**kwargs)
    elif agentType == "msStraightMU256":
        return msStraightMU.straightMU256(**kwargs)
    elif agentType == "msTargetPrice8":
        return msTargetPrice.targetPrice8(**kwargs)
    elif agentType == "msTargetPrice64":
        return msTargetPrice.targetPrice64(**kwargs)
    elif agentType == "msTargetPrice256":
        return msTargetPrice.targetPrice256(**kwargs)
    elif agentType == "msCondLocalGreater" or agentType == "condLocalGreater":
        return msCondMVLocal(**kwargs)
    elif agentType == "jointLocal":
        return jointLocal(**kwargs)
    else:
        raise ValueError("Unknown Agent Type {0}".format(agentType))
    
        
    