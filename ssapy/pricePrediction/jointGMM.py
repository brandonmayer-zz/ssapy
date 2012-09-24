import numpy
import sklearn.mixture
from scipy.stats import norm

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import itertools
import time
import os

class jointGMM(object):
    """
    A wrapper around sklearn.mixture.GMM to add some additional functionality
    """
    def __init__(self,**kwargs):
        self.minPrice        = kwargs.get('minPrice',0)
        self.maxPrice        = kwargs.get('maxPrice',50)
        
        self.gmm             = None
        
        # parameters for sklearn.mixture.GMM
        self.covariance_type = kwargs.get('covariance_type','full')
        self.random_state    = kwargs.get('random_state',None)
        self.thresh          = kwargs.get('thresh',0.01)
        self.min_covar       = kwargs.get('min_covar',0.001)
        self.n_iter          = kwargs.get('n_itr',100)
        self.n_init          = kwargs.get('n_init',1)
        self.params          = kwargs.get('params','wmc')
        self.init_params     = kwargs.get('init_params','wmc')
        
    def sample(self, **kwargs):
        if self.gmm == None:
            raise ValueError("jointGMM.sample(...) - gmm is not yet defined")
        
        minPrice  = kwargs.get('minPrice',self.minPrice)
        maxPrice  = kwargs.get('maxPrice',self.maxPrice)
        
        n_samples = kwargs.get('n_samples', 1)
        random_state = kwargs.get('random_state')
        
        samples = numpy.zeros((n_samples, self.gmm.means_.shape[1]))
                
        # inefficient way of restricting sample domain
        # to valid prices but works for now...
        idx = 0
        while idx < n_samples:
            s = self.gmm.sample(1,random_state)[0]
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
        self.params          = kwargs.get('params','wmc')
        self.init_params     = kwargs.get('init_params','wmc')
    
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
        
        self.gmm = clfList[argMinAic]
        
        if verbose:
            print 'Finished aicFit(...) in {0} seconds'.format(time.time()-start)
            print 'Minimum AIC = {0}'.format(aicList[argMinAic])
            print 'Number of components = {0}'.format(compRange[argMinAic])
                
        return clfList[argMinAic], aicList, compRange
    
    def pltMargDist(self,**kwargs):
        
        oFile    = kwargs.get('oFile')
        nPts     = kwargs.get('nPts',10000)
        minPrice = kwargs.get('minPrice',self.minPrice)
        maxPrice = kwargs.get('maxPrice',self.maxPrice)
        colors   = kwargs.get('colors')
        title   = kwargs.get('title', "Marginals of Joint Gaussian")
        xlabel  = kwargs.get('xlabel', "price")
        ylabel  = kwargs.get(r"$p(closing price)$")
        
        
        
        nComps = self.gmm.means_.shape[0]
        nGoods = self.gmm.means_.shape[1]
        if not colors:
            cmap = plt.cm.get_cmap('hsv')
            colorStyles = [cmap(i) for i in numpy.linspace(0,0.9,nGoods)]
            colorCycle = itertools.cycle(colorStyles)
        else:
            colorCycle = itertools.cycle(colors)
        
        X = numpy.linspace(minPrice, maxPrice, nPts)
        
        fig = plt.figure()
        ax  = plt.subplot(111)
        for goodIdx in xrange(nGoods):
            margDist = numpy.zeros(X.shape[0])
            for (w,mean,cov) in zip(self.gmm.weights_,self.gmm.means_, self.gmm.covars_):
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
        
        if not oFile:
            plt.show()
        else:
            plt.savefig(oFile)
            
    def plt(self,**kwargs):
        minPrice = kwargs.get('minPrice',self.minPrice)
        maxPrice = kwargs.get('maxPrice',self.maxPrice)
        oFile   = kwargs.get('oFile')
        
        verbose = kwargs.get('verbose',True)
        
        if self.gmm.means_.shape[1] == 2:
            if verbose:
                print 'plotting joint distribution'
        
            
            f = plt.figure()
            ax = f.add_subplot(111,projection='3d')
            ax.view_init(26,-142)
            
            X = numpy.arange(minPrice,maxPrice,0.5)
            Y = numpy.arange(minPrice,maxPrice,0.5)
            xx,yy = numpy.meshgrid(X, Y)
            s = numpy.transpose(numpy.atleast_2d([xx.ravel(),yy.ravel()]))

            Z = numpy.exp(self.gmm.eval(s)[0].reshape(xx.shape))
            
            surf = ax.plot_surface(xx, yy, Z, rstride=1, cstride=1, cmap=cm.jet,
                                   linewidth=0, antialiased=True)
                        
#                f.colorbar(surf,shrink=0.5,aspect=5)
            
            nComp = self.gmm.means_.shape[0]
            ax.set_title("nComp = {0}".format(nComp))
            
            if not oFile:
                plt.show()
            else:
                plt.savefig(oFile)
        else:
            print 'Cannot plot joint distribution with dimension greater than 2.'
            

        
        