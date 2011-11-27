import pickle
import numpy

class pointSCPP(object):
    """
    Class wrapper for point self confirming price predictions
    """
    def __init__(self, pointPricePrediction = None):
        
        if isinstance(pointPricePrediction,numpy.ndarray):
            if numpy.atleast_2d(pointPricePrediction).shape[0] == 1:
                self.data = pointPricePrediction
                self.m = numpy.atleast_2d(self.data).shape[1]
            else:
                print "----Warning----"
                print "pointSCPP.__init__"
                print "pointPricePrediction must be a 1d array"
                print "self.data = None"
                self.data = None
        elif pointPricePrediction == None:
            self.data = None
            self.m = None
        else:
            print "----Warning----"
            print "pointSCPP.__init__"
            print "pointPricePrediction must be a numpy.ndarray"
            print "self.data = None"
            self.data = None
                    
    @staticmethod
    def type():
        return "pointSCPP"
    
    def savePickle(self,f):
        """
        Function to serialize class to binary file
        """
        assert (isinstance(f,basestring) or
                isinstance(f,file) ),\
                "pointSCPP.savePickle must provide a filename string or file object."
        if isinstance(f,basestring):
            pickle.dump(self,open(f,'wb'))
            
        elif isinstance(f,file):
            pickle.dump(self,f)
        
        
    def loadPickle(self,f):
        """
        Function to load data from serialized class instance
        """
        if isinstance(f,basestring):
            
            temp = pickle.load(open(filename,'rb'))
            if temp.type() == self.type():
                self.data   = temp.data
                self.m      = temp.m
            else:
                print "----Warning----"
                print "{0}::loadPickle".format(self.type())
                print "Specified file is not compatible with instance type."
                print "Load Failed"
                return False
            
        elif isinstance(f,file):
            
            temp = pickle.load(f)
            if temp.type() == self.type():
                self.data   = temp.data
                self.m      = temp.m
            else:
                print "----Warning----"
                print "{0}::loadPickle".format(self.type())
                print "Specified file is not compatible with instance type."
                print "Load Failed"
                return False
            
        else:
            print "----ERROR----"
            print "{0}::loadPickle".format(self.type())
            print "Cannot load pickled instance"
            print "Must Provide filename string or file object"
            return False
            
                
    