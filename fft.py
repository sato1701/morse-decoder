import numpy as np
from statistics import variance
import wave
from math import sqrt, pi, exp, sin, cos
from scipy import fftpack, signal
import matplotlib.pyplot as plt
import struct
import sys

fname = sys.argv[1]
N = 512
freq = 48000

window = np.hanning(N)
freqList = np.fft.rfftfreq(N, d=1/freq)
peakList = []

waveFile = wave.open(fname, 'r')
sampleSize = waveFile.getsampwidth()
buffer = waveFile.readframes(-1)
rawdata = np.frombuffer(buffer, dtype="int32")
if(waveFile.getnchannels() == 2):
    dataL = rawdata[::2]
    dataR = rawdata[1::2]
    data = (dataL + dataR)/pow(2,31)
else:
    data = rawdata
waveFile.close()

x_range = np.arange(0, len(data), 64)
len_data = len(data)
tmp = []

for i in x_range:
    if N > len_data-i:
        break
    fftData = np.fft.rfft(data[i : i+512]*window)
    ret = np.abs(fftData)/(N/2)
    var = np.var(ret, ddof=0)
    tmp.append(var)
#        if var > 1.3*pow(10, 15):
#            tmp.extend(data[i:i+480000])
#            flag = 625
#    if(var > pow(10,15)):
#        peak = np.argmax(ret)
#        peakList.append(freqList[peak])
#    else:
#        peakList.append(0)
#plt.pcolormesh(freqList, x_range/48000, tmp)

for i in range(len(tmp)):
    if tmp[i] > 1.2*pow(10, 15):
        tmp[i] = 1
    else:
        tmp[i] = 0

plt.plot(tmp, linestyle='', marker='o')
plt.show()
