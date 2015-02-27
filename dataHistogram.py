# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 14:09:03 2015

@author: s113094
"""

from QRNG import createHistogram
import time

start_time = time.clock()
#createHistogram("ScopeData/1064/scopedark",100)
createHistogram("ScopeData/1064/M2zoomed",100)

print "time elapsed: %.2f seconds" % (time.clock()-start_time)