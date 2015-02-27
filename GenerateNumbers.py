# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 15:20:03 2015

@author: s113094
"""

from __future__ import print_function,division
import PyFFT
import QRNG
import time
import numpy as np
#from math import *
#import matplotlib.pyplot as plt

#%%
#Import data
start_time1 = time.clock()

my_dir = "Data/"
my_file = "1550-2.0ND"
file_name=my_dir+my_file
x,t,dt = PyFFT.importData(file_name)   
fs = len(t)/dt

print("Import time: %.2f s"%(time.clock()-start_time1))

#%%

start_time2 = time.clock()
#rejection_zone = 0.00005
rejection_zone = 0

# Sample rate and desired cutoff frequencies (in Hz).
BW = 1 * 10**6 #Cutoff bandwidth
f = 50*(10**6) #Downmixing frequency

#Down mix, lowpass
y = QRNG.downmixSignal(x,f,t,BW,fs,True,5,'bessel') 

#Down sample to flat autocorr.
#Run in downmix.py to check how much to down-sample.
nth = 200
yd = y[::nth]

#Histogram of data
#QRNG.createHistogram(yd,bins=80,rejected=rejection_zone)

#bits = np.array([QRNG.generateBit2(X,rejection_zone) for X in yd])
#accepted_bits = bits[bits != -1]
accepted_bits = QRNG.generateBit(yd,rejection_zone)

lb = len(yd)
lb0 = len(accepted_bits[accepted_bits==0])
lb1 = len(accepted_bits[accepted_bits==1])
lba = len(accepted_bits) #Accepted bits
lbr = len(yd)-lba #Rejected bits

#bit_dir_str = my_dir+"/Bits/bits-%s.txt"%my_file
#resultfile = open(bit_dir_str, 'w')
#for my_bit in accepted_bits: print(my_bit,file=resultfile)
#resultfile.close()

print("Bits = 0: %d" %lb0)
print("Bits = 1: %d" %lb1)
print("Accepted bits: %d" %lba)
print("Rejected bits: %d" %lbr)
if lba == 0:
    print("Rejected all bits.")
else:
    print("Percentage of bits which are 0: %.4f" %((1-float(lb0)/lba)*100))
    print("Rejected percentage of bits: %.3f" %((lbr/lb)*100))
   
print("Elapsed time of post-processing: %.2f s"%(time.clock()-start_time2))