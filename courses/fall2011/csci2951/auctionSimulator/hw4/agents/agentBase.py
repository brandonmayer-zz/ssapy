'''
This is /auctionSimulator/hw4/agents.py

Author: Brandon A. Mayer
Date: 11/13/2011

A file containing agents and auctions to reproduce Yoon and Wellman
'''
#import itertools
#import numpy
#import operator
#import random 
#import sys,traceback

class agentBase(object):
    nextId = 0
    def __init__(self, name="Anonymous"):
        self.name = name
        self.id = nextID
        nextID += 1

    def id(self):
        return self.id
    
    @staticmember
    def type():
        return "agentBase"    