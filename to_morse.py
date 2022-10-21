import numpy as np
import wave
from scipy import fftpack
import sys
import matplotlib.pyplot as plt
from decoder import decode

fname = sys.argv[1]
N = 512
freq = 48000

def counter(data):
    count = 5
    countList = []

    noise_count = 5
    start_flag = False
    state = 1
    not_noise_num = 10

    for i in range(len(data)-1):
        if start_flag == False:
            if data[i] == 1:
                noise_count -= 1
                if noise_count == 0:
                    start_flag = True
            else:
                noise_count = 5
            continue
        else:
            if data[i] == state:
                count += 1 + noise_count
                noise_count = 0
            else:
                noise_count +=1
#                if count >= not_noise_num:
#                    state = abs(state-1)
#                    countList.append(count)
#                    count = 0
                if noise_count >= not_noise_num-1:
                    state = abs(state-1)
                    countList.append(count)
                    count = not_noise_num-1
                    noise_count = 0
    return countList

def toMorse(data):
    ret = []
    tmp = ""
    isChar = True
#    for i in l:
#        if(tmp == i):
#            count += 1
#        elif(count != 0):
#            countList.append(count)
#            count = 0
#        tmp = i

    dotLen = 20

    for i in data:
        if(isChar):
            if(i <= dotLen*2):
                tmp += '.'
            else:
                tmp += '-'
        else:
            if(dotLen*2 < i <= dotLen*5):
                ret.append(tmp)
                tmp = ''
            elif(dotLen*5 < i):
                ret.append(tmp)
                ret.append('\n')
                tmp = ''
        isChar = not isChar
    return ret


if __name__ == '__main__':
    window = np.hanning(N)
    freqList = np.fft.rfftfreq(N, d=1/freq)

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

    sampleNum = 64
    len_data = len(data)
    peakList = np.full(int(len_data/sampleNum), 0, dtype='int8')

    for i in range(0, len(data), sampleNum):
        if(len_data-i < N):
            break
        fftData = np.fft.rfft(data[i:i+N]*window)
        ret = np.abs(fftData)/(N/2)
        var = np.var(ret, ddof=0)

        if(var > 1.0*pow(10, 15)):
            peakList[int(i/sampleNum)] = 1
#       peak = np.argmax(ret)
#       peakList.append(freqList[peak])
#    else:
#        peakList.append(0)
#ans = []
#relation_check(peakList)
#stop
    morseList = toMorse(counter(peakList))
    print(morseList)
    print(decode(morseList))
