# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 17:27:22 2015

@author: s113094
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 14:29:10 2015

@author: s113094
"""

import PyFFT
import QRNG
import numpy as np
from math import *
import matplotlib.pyplot as plt

#%%
#Import data
file_name="ScopeData/1064/M2zoomed"
x,t,dt = PyFFT.importData(file_name)   
fs = len(t)/dt

#%%
#Plot the spectrum.
plt.figure(1)
freq,ftx=PyFFT.doFFT(x,dt)
#PyFFT.plotFFT(freq,ftx)

#%%
#Down mix, lowpass

# Sample rate and desired cutoff frequencies (in Hz).
BW = 2 * 10**6 #Cutoff bandwidth
f = 40*(10**6) #Downmixing frequency
y = QRNG.downmixSignal(x,f,t,BW,fs,True,5,'bessel') 

plt.figure(2)
freq,fty=PyFFT.doFFT(y,dt)

#PyFFT.plotFFT(freq,fty)

#%%

#Auto correlation before down sampling
auto = PyFFT.autocorr(y)
#%%
plt.figure(3)
plt.plot(auto,'r-')

plt.axis([0,300,-0.1,1])
plt.show()

#%%
#Down sample to flat autocorr.
nth = 200
yd = y[::nth]

#%%

#Auto correlation after down sampling
autod = PyFFT.autocorr(yd)

#%%
plt.figure(4)
plt.plot(autod,'r*')

plt.axis([0,10,-0.1,1])
plt.show()

#%%
plt.figure(5)
freq,ftyd=PyFFT.doFFT(yd,dt,3000)
PyFFT.plotFFT(freq,ftyd)