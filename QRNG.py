# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 12:21:06 2015

@author: s113094
"""

from __future__ import division
#from math import *
import numpy as np
#from pylab import *
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, bessel
from scipy import integrate
import scipy.special as sp

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='lowpass', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
    
def bessel_lowpass_filter(data,cutoff,fs,order=5):
    nyq = 0.5*fs
    normal_cutoff = cutoff/nyq
    b,a = bessel(order,normal_cutoff,btype='lowpass',analog=False)
    return lfilter(b,a,data)

def downmixSignal(x,f,t,BW,fs,lfilt=True,order=5,filt_type='bessel'):
    s = np.sin(2*np.pi*f*t)         #Correct frequency to angular freq.
    x = x*s
    if lfilt == True:
        if filt_type == 'butter':
            x = butter_lowpass_filter(x,BW,fs,order)
        else:
            x = bessel_lowpass_filter(x,BW,fs,order)       
    return x
    
def generateBit(x,dt=0):
                                    #Assumes mean(Xm)=0
#    x = Xm - data_mean
    idx = np.abs(x) > dt            #Generate a mask
    x = x[idx]                      #Apply mask 
    #Using Signnum function to convert to -1 or 1.
    return (np.sign(x)+1)//2         #Convert -1 to 0 and +1 stays +1.
    
def generateBit2(Xm,dt=0):
    #Assumes mean(Xm)=0
#    x = Xm - data_mean
    if np.abs(Xm) <= dt:
        return -1
    if Xm > dt:
        return 1
    else:
        return 0


def gaussian(x,mu=1.0,var=1.0):
    return np.exp(-np.power(x-mu,2.)/(2*var))/np.sqrt(2*np.pi*var)
  
def Perror(Delta,var,SNR=8.0):
    Pcorr = lambda x: np.exp(-np.power(x,2)/(
        2*var))*sp.erfc(np.sqrt((SNR-1)/(2*var))*x)
        
    Pe = np.arctan(1/np.sqrt(SNR-1))/np.pi - integrate.quad(
        Pcorr,0,Delta)[0]/np.sqrt(2*np.pi*var)
    return Pe

def Preject(Delta,var):
    return sp.erf(Delta/np.sqrt(2*var))

def createHistogram(my_data,bins=10,norm=True,rejected=0):

    data_var = np.var(my_data)
    
    xmin=min(my_data)
    xmax=max(my_data)
    xval = np.linspace(xmin,xmax,100)
    yval = gaussian(xval,0,data_var)
    
    
    plt.hist(my_data,bins=bins,normed=norm)
    plt.plot(xval,yval,color='r')
    if np.abs(rejected) > 0:
        plt.axvspan(-rejected,rejected,facecolor='g',alpha=0.5)
    plt.show()
    print "Variance: %.3f"%data_var
    
    