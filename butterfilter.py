# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 14:29:10 2015

@author: s113094
"""

from scipy.signal import butter, lfilter
import PyFFT


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


if __name__ == "__main__":
    import numpy as np
    from math import *
    from pylab import savetxt,column_stack
    import matplotlib.pyplot as plt

    # Sample rate and desired cutoff frequencies (in Hz).
    lowcut = 49*10**6
    highcut = 51*10**6

    # Filter a noisy signal.
    file_name="ScopeData/1064/M2zoomed"
    x,t,dt = PyFFT.importData(file_name)   
    fs = len(t)/dt  
    
    plt.clf
    plt.figure(1)
    plt.plot(t,x,'.', label='Noisy signal')
    y = butter_bandpass_filter(x, lowcut, highcut, fs, order=6)
    plt.plot(t,y,'r.', label='Filtered signal')
    plt.legend(loc='upper left')
    plt.show()
    
    #Export the filtered data
#    export_file_name = file_name+"Filtered"
#    savetxt(export_file_name+".csv",column_stack((t,y)),delimiter=",")
    
    plt.figure(2)
    freq,fty=PyFFT.doFFT(y,dt)
    PyFFT.plotFFT(freq,fty)
    
    plt.figure(3)
    freq,ftx=PyFFT.doFFT(x,dt)
    PyFFT.plotFFT(freq,ftx)