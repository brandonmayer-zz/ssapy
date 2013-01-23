from .averageMU import averageMU8, averageMU64, averageMU256
from .straightMU import straightMUa, straightMU8, straightMU64, straightMU256
from .straightMV import straightMV
from .targetMU import targetMU8,targetMU64,targetMU256
from .targetMV import targetMV
from .targetMVS import targetMVS
from .targetPrice import targetPrice8, targetPrice64, targetPrice256
from .jointLocal import jointLocal, jointLocalMc
from .condLocal import condLocal, condLocalGreater
from .margLocal import margLocal

def strategyFactory(ss = None):
    """
    Function which returns a strategy function pointer given
    a strategy type string.
    """
    if ss == 'averageMU8':
        return averageMU8
    elif ss == 'averageMU64':
        return averageMU64
    elif ss == 'averageMU256':
        return averageMU256
    elif ss == 'straightMUa':
        return straightMUa
    elif ss == 'straightMU8':
        return straightMU8
    elif ss == 'straightMU64':
        return straightMU64
    elif ss == 'straightMU256':
        return straightMU256
    elif ss == 'straightMV':
        return straightMV
    elif ss == 'targetMU8':
        return targetMU8
    elif ss == 'targetMU64':
        return targetMU64
    elif ss == 'targetMU256':
        return targetMU256
    elif ss == 'targetMV':
        return targetMV
    elif ss == 'targetMVS':
        return targetMVS
    elif ss == 'targetPrice8':
        return targetPrice8
    elif ss == 'targetPrice64':
        return targetPrice64
    elif ss == 'targetPrice256':
        return targetPrice256
    elif ss == 'jointLocal':
        return jointLocal
    elif ss == 'jointLocalMc':
        return jointLocalMc
    elif ss == 'condLocal':
        return condLocal
    elif ss == 'condLocalGreater':
        return condLocalGreater
    elif ss == 'margLocal':
        return margLocal
    else:
        return ValueError('Unknown Strategy Type {0}.'.format(ss))
    
