import numpy
import sklearn.mixture
from scipy.stats import norm

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import itertools
import time
import os

class jointGMM(sklearn.mixture.GMM):
    """
    A wrapper around sklearn.mixture.GMM to add some additional functionality
    """
    def __init__(self,**kwargs):
        self.minPrice        = kwargs.get('minPrice',0)
        self.maxPrice        = kwargs.get('maxPrice',numpy.float('inf'))
        
#        self.gmm             = None

        super(jointGMM,self).__init__(n_components = kwargs.get('n_components',1),
                                      covariance_type = kwargs.get('covariance_type','full'),
                                      random_state    = kwargs.get('random_state',None),
                                      min_covar       = kwargs.get('min_covar',1e-3),
                                      n_iter           = kwargs.get('n_iter',100),
                                      n_init          = kwargs.get('n_init',1),
                                      params          = kwargs.get('params','wmc'),
                                      init_params     = kwargs.get('init_params','wmc') )
        
    def sample(self, **kwargs):
        
        minPrice  = kwargs.get('minPrice',self.minPrice)
        maxPrice  = kwargs.get('maxPrice',self.maxPrice)
        
        n_samples = kwargs.get('n_samples', 1)
        
        random_state = kwargs.get('random_state',self.random_state)
        
        sampleFncPtr = super(jointGMM,self).sample
        
        samples = numpy.zeros((n_samples, self.means_.shape[1]))
                
        # inefficient way of restricting sample domain
        # to valid prices but works for now...
        idx = 0
        while idx < n_samples:
            s = sampleFncPtr(1,random_state)[0]
            if ~numpy.any(s > maxPrice) and ~numpy.any(s < minPrice):
                samples[idx,:] = s
                idx += 1
                
        return samples
    
#    def aicFit(self, X, compRange = range(1,6), minCovar = 9, covarType = 'full', verbose = True):
    def aicFit(self, **kwargs):
        X               = kwargs.get('X')
        compRange       = kwargs.get('compRange',numpy.arange(1,6))
        
        #accept new mixture model params as arguments
        #and store on instance
        self.covariance_type = kwargs.get('covariance_type', self.covariance_type)
        self.random_state    = kwargs.get('random_state',self.random_state)
        self.thresh          = kwargs.get('thresh',self.thresh)
        self.min_covar       = kwargs.get('min_covar', self.min_covar)
        self.n_iter          = kwargs.get('n_itr',self.n_iter)
        self.n_init          = kwargs.get('n_init',self.n_init)
        self.params          = kwargs.get('params',self.params)
        self.init_params     = kwargs.get('init_params',self.init_params)
    
        verbose         = kwargs.get('verbose',True)
        
        if verbose:
            print 'starting aicFit(...)'
            print 'compRange = {0}'.format(compRange)
            print 'minCovar  = {0}'.format(self.min_covar)
            start = time.time()
            
        clfList = [sklearn.mixture.GMM(n_components    = c, 
                                       covariance_type = self.covariance_type,
                                       random_state    = self.random_state,
                                       min_covar       = self.min_covar,
                                       thresh          = self.thresh,
                                       n_iter          = self.n_iter,
                                       n_init          = self.n_init,
                                       params          = self.params,
                                       init_params     = self.init_params)\
                                       for c in compRange] 
                                       
        
        [clf.fit(X) for clf in clfList]
        
        aicList = [clf.aic(X) for clf in clfList]
        
        argMinAic = numpy.argmin(aicList)
        
        # set the data of this class associated with the 
        # derived class to match the fitted distribution
        self.__dict__.update(clfList[argMinAic].__dict__)
        
        if verbose:
            print 'Finished aicFit(...) in {0} seconds'.format(time.time()-start)
            print 'Minimum AIC = {0}'.format(aicList[argMinAic])
            print 'Number of components = {0}'.format(compRange[argMinAic])
                
        return clfList[argMinAic], aicList, compRange
    
    def pltMargDist(self,**kwargs):
        
        oFile    = kwargs.get('oFile')
        nPts     = kwargs.get('nPts',1000)
        minPrice = kwargs.get('minPrice',0)
        maxPrice = kwargs.get('maxPrice',50)
        colors   = kwargs.get('colors')
        title   = kwargs.get('title', "Marginals of Joint Gaussian")
        xlabel  = kwargs.get('xlabel', "price")
        ylabel  = kwargs.get('ylabel', r"$p(closing price)$")
        
        
        
        nComps = self.means_.shape[0]
        nGoods = self.means_.shape[1]
        if not colors:
            cmap = plt.cm.get_cmap('hsv')
            colorStyles = [cmap(i) for i in numpy.linspace(0,0.9,nGoods)]
            colorCycle = itertools.cycle(colorStyles)
        else:
            colorCycle = itertools.cycle(colors)
        
        X = numpy.linspace(minPrice, maxPrice, nPts)
        
        fig = plt.figure(dpi=100)
        ax  = plt.subplot(111)
        for goodIdx in xrange(nGoods):
            margDist = numpy.zeros(X.shape[0])
            for (w,mean,cov) in zip(self.weights_,self.means_, self.covars_):
                margMean = mean[goodIdx]
                margCov  = cov[goodIdx,goodIdx]
                rv = norm(loc=margMean, scale=numpy.sqrt(margCov))
                margDist += w*rv.pdf(X)
            plt.plot(X,margDist,color=next(colorCycle),label = 'good {0}'.format(goodIdx))
            
        
        leg = ax.legend(loc = 'best',fancybox = True)
        leg.get_frame().set_alpha(0.5)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        if oFile is None:
            plt.show()
        else:
            plt.savefig(oFile)
            
    def plt(self,**kwargs):
        minPrice = kwargs.get('minPrice',0)
        maxPrice = kwargs.get('maxPrice',50)
        oFile   = kwargs.get('oFile')
        xlabel  = kwargs.get('xlable',r'$q_1$')
        ylabel  = kwargs.get('ylable',r'$q_2$')
        zlabel  = kwargs.get('zlabel',r'$p(q_1,q_2)$')
        
        verbose = kwargs.get('verbose',True)
        
        if self.means_.shape[1] == 2:
            if verbose:
                print 'plotting joint distribution'
        
            
            f = plt.figure(dpi=100)
            ax = f.add_subplot(111,projection='3d')
            ax.view_init(26,-142)
            
            X = numpy.arange(minPrice,maxPrice,0.5)
            Y = numpy.arange(minPrice,maxPrice,0.5)
            xx,yy = numpy.meshgrid(X, Y)
            s = numpy.transpose(numpy.atleast_2d([xx.ravel(),yy.ravel()]))

            Z = numpy.exp(self.eval(s)[0].reshape(xx.shape))
            
            surf = ax.plot_surface(xx, yy, Z, rstride=1, cstride=1, cmap=cm.jet,
                                   linewidth=0, antialiased=True)
            
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_zlabel(zlabel)
                        
#                f.colorbar(surf,shrink=0.5,aspect=5)
            
            nComp = self.means_.shape[0]
            ax.set_title("nComp = {0}".format(nComp))
            
            if not oFile:
                plt.show()
            else:
                plt.savefig(oFile)
        else:
            print 'Cannot plot joint distribution surface with dimension greater than 2.'
            

        
        