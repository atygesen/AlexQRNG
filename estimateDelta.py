# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 14:09:36 2015

@author: s113094
"""

from __future__ import division
import PyFFT
import QRNG
import numpy as np
import matplotlib.pyplot as plt

#%%
#Import data
my_dir = "Data/"
my_file = "1550-2.0ND"
file_name=my_dir+my_file
x,t,dt = PyFFT.importData(file_name)   
fs = len(t)/dt

#%%

## Sample rate and desired cutoff frequencies (in Hz).
#BW = 1 * 10**6 #Cutoff bandwidth
#f = 50*(10**6) #Downmixing frequency
#
##Down mix, lowpass
#y = QRNG.downmixSignal(x,f,t,BW,fs,True,5,'bessel') 
#
##Down sample to flat autocorr.
##Run in downmix.py to check how much to down-sample.
#nth = 200
#yd = y[::nth]

Vm = np.var(x)
fig = plt.figure(1)
#SNR_log = np.arange(2.,10,1)
#SNR_list = np.power(10.,SNR_log/10)
SNR_list = np.arange(2.,15,2)
N = len(SNR_list)
i = 0

fig = plt.figure(1)
fig2 = plt.figure(2)
ax = fig.add_subplot(111)
ax2 = fig2.add_subplot(111)
cmap = plt.cm.get_cmap('jet')
deltalist = np.linspace(0,1500*Vm,100)


for SNR in SNR_list:
    c = cmap(float(i)/(N-1))
    i += 1
    p_error = np.array([QRNG.Perror(Delta,Vm,SNR) for
        Delta in deltalist])*100
    p_reject = QRNG.Preject(deltalist,Vm)*100
    ax.plot(p_error,p_reject,label="SNR = %.2f"%SNR,color=c)
    ax2.plot(deltalist,p_error,label="SNR = %.2f"%SNR,color=c)

ax.set_xlabel('Pe [%]')
ax.set_ylabel('Rejected bits [%]')

ax2.set_xlabel('$\Delta$')
ax2.set_ylabel('Pe[%]')


plt.figure(1)
plt.legend(loc='lower left');
plt.xscale('log')

plt.figure(2)
plt.xscale('log')
plt.legend(loc='upper right')

plt.show()
