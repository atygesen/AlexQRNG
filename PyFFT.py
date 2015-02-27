# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 15:14:25 2015

@author: s113094"""

import numpy as np
import quik.samples.fft as qfft
from math import floor
import matplotlib.pyplot as plt
import pandas as pd

def _autocorf(x):
    fftx = np.fft.fft(x)
    return np.fft.fftshift(np.fft.ifft(fftx
        *np.conjugate(fftx)))[fftx.size/2:]

def autocorr(x):
    corx = _autocorf(x)
    x0 = corx[0]
    return corx/x0

def importData(file_name):
    header_size = 21
    my_data = pd.read_csv(file_name+".csv", delimiter=','
        , skiprows=header_size,header=None).values
    t = np.array(my_data[:,0])
    dt = t[-1]-t[0] #Delta Time
    my_data = np.array(my_data[:,1])
    data_mean = np.mean(my_data) #DC offset
    my_data -= data_mean
    return my_data,t,dt
    
    
def exportFFTdata(file_name,freq,x):
    #    Export the FFT dataset
    data_mean = np.mean(x)
    mean_string = "%.5f" % data_mean
    export_file_name = file_name+"FFT.csv"
    np.savetxt(export_file_name,np.column_stack((freq,x)),delimiter=",",
            header=mean_string)
    
    
def plotFFT(freq,fft_channel,xax='log',yax='log'):
    plt.plot(freq,fft_channel)
    plt.yscale(xax)
    plt.xscale(yax)
    plt.show()
    
def doFFT(my_data,dt,fres = 300000):
#    #file_name=string
#    header_size = 21
#    
#    my_data = loadtxt(file_name+".csv", delimiter=',', skiprows=header_size)
#    dt = my_data[-1,0]-my_data[0,0] #Delta Time
#    
#    my_data = my_data[:,1]
#    data_mean = mean(my_data) #DC offset
#    my_data -= data_mean
#    mean_string = "%.5f" % data_mean
#    
#    print "testing "+file_name+".csv"+" at "+mean_string+" DC voltage."
    
    points=float(len(my_data))
    fres = float(fres)
    
     # compute sample partitioning
    fs = points/dt
    Npartition = floor(fs / fres)
    if ((Npartition % 2) == 1):
        Npartition += 1
    
    fres = fs / Npartition
    # compute fft
    window = qfft.hft116d(Npartition)
    fft_channel = qfft.fft_welch(my_data, fs, Npartition, window, 0.782)[3]
    # Select [3] for the density power spectrum divided by fres.
    #output = u^2/RBW
    #Standard overlap: 0.782    
    
    freq = np.arange(0,Npartition/2)*fres
    
    return freq,fft_channel
    
    
    
#if __name__ == "__main__":
#    file_name="ScopeData/1064/M2zoomed"
#    x,t,dt = importData(file_name)
#    freq,fft_data = doFFT(x,dt)
#    plotFFT(freq,fft_data)