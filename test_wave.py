import wave
import numpy as np
from math import sqrt, pi, exp, sin, cos
from scipy import fftpack
import matplotlib.pyplot as plt
import struct

fname = './data/low_speed.wav'

waveFile = wave.open(fname, 'r')
sampleSize = waveFile.getsampwidth()

print(sampleSize)

buffer = waveFile.readframes(-1)
rawdata = np.frombuffer(buffer, dtype="int32")
if(waveFile.getnchannels() == 2):
    dataL = rawdata[::2]
    dataR = rawdata[1::2]
data = (dataL + dataR)/pow(2,31)
waveFile.close()

#plt.plot(data)
#plt.show()
