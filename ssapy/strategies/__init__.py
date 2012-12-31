from straightMV import straightMV
from straightMU import straightMU8, straightMU64, straightMU256
from margLocalBid import margLocalBid

strategyDict = {'straightMV'   : straightMV,
                'straightMU8'  : straightMU8,
                'straightMU64' : straightMU64,
                'straightMU256': straightMU256,
                'margLocalBid' : margLocalBid}