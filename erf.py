# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 11:51:19 2015

@author: s113094
"""

#from math import *
import matplotlib.pyplot as plt
import numpy as np
import time
import QRNG
from pylab import *

start_time = time.clock()
x = np.linspace(-4,4,100)
#y = [Ym(xm,0.5) for xm in x]
#y = map(Ym,x)
y = QRNG.Ym(x)

#plt.plot(x,y,color='r')


file_name="ScopeData/1064/M2zoomed"
header_size = 21
my_data = loadtxt(file_name+".csv", delimiter=',', skiprows=header_size)
my_data = my_data[:,1]



#my_data = np.random.normal(0,1,2000)


data_mean = mean(my_data)
data_var = np.var(my_data)

my_data -= data_mean

bin_data = np.array([QRNG.generateBit(Xm,0,0.001) for Xm in my_data])
bin_data = bin_data[bin_data != -1]

print "Rejected data percent: %.2f" % ((1-float(len(bin_data))/len(my_data))*100)

print time.clock()-start_time," seconds"