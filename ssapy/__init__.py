import numpy
import itertools
import datetime

from .pricePrediction.dokHist import dokHist

from .agents.marketSchedule import listRevenue as msListRevenue

from .agents.marketSchedule import \
    randomValueVector as msRandomValueVector
    
from .util import listBundles

from .agents.agentFactory import agentFactory

def timestamp_():
    now = datetime.datetime.now()
    return "{0}_{1:02}_{2:02}_{3:02}_{4:02}_{5:02}_{6:06}".\
        format(now.year,now.month,now.day,now.hour,now.minute,now.second,now.microsecond)