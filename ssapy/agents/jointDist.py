from sklearn.mixture import GMM
from ssapy.pricePrediction.util import drawJointGMM
from ssapy.agents.simYW import simYW
from ssapy.agents.straightMV import straightMV

class jointDistAgent(simYW):
    vaild_ss = ['averageMU', 'straightMV', 'targetMV', 'targetMVS','targetPrice']
    def __init__(self,**kwargs):
        super(jointDistAgent,self).__init__(**kwargs)
        
        self.nSamples = kwargs.get('nSamples')
        
        self.pp = kwargs.get('pp')
        
        self.ss = kwargs.get('ss')
        
    def bid(self,**kwargs):
        nSamples = kwargs.get('nSamples',self.nSamples)
        ss       = kwargs.get('ss',self.ss)
        pp       = kwargs.get('pp',self.pp)
        m        = kwargs.get('m', self.m)
        v        = kwargs.get('v', self.v)
        l        = kwargs.get('l', self.l)
        vmin     = kwargs.get('vmin',self.vmin)
        vmax     = kwargs.get('vmax',self.vmax)
        
        if ss not in jointDistAgent.vaild_ss:
            raise ValueError("-----ERROR-----\n" +\
                              "In jointDistAgent.bid(...)\n" +\
                              "{0} not in valid Strategy profile list {1}".format(jointDistAgent.vaild_ss))
        
        bundles        = simYW.allBundles(m)
        valuation      = simYW.valuation(bundles, v, l)
        samples        = drawJointGMM(pp, nSamples, vmin, vmax)
        expectedPrices = numpy.mean(samples,0)
        
        bids = None
        if ss == "averageMU":
            pass
            
        elif ss == "straightMV":
            bids = straightMV.SS(pointPricePrediction = expectedPrices,
                                 bundles              = bundles,
                                 valuation            = valuation,
                                 l                    = l)
        
        elif ss == "targetMV":
            pass
        
        elif ss == "targetMVS":
            pass
        
        elif ss == "targetPrice":
            pass
        
        return bids
        
    @staticmember
    def SS(**kwargs):
        pass
        
        
    