import numpy as np
import wave
from math import sqrt, pi, exp, sin, cos
from scipy import fftpack, signal
import matplotlib.pyplot as plt
import struct
import sys

fname = sys.argv[1]
N = 512
freq = 48000

def decode(l):
    morseDict = {
    ".-": "A",     "-...": "B",   "-.-.": "C",
    "-..": "D",    ".": "E",      "..-.": "F",
    "--.": "G",    "....": "H",   "..": "I",
    ".---": "J",   "-.-": "K",    ".-..": "L",
    "--": "M",     "-.": "N",     "---": "O",
    ".--.": "P",   "--.-": "Q",   ".-.": "R",
    "...": "S",    "-": "T",      "..-": "U",
    "...-": "V",   ".--": "W",    "-..-": "X",
    "-.--": "Y",   "--..": "Z",
    "-----": "0",  ".----": "1",  "..---": "2",
    "...--": "3",  "....-": "4",  ".....": "5",
    "-....": "6",  "--...": "7",  "---..": "8",
    "----.": "9",
    "-....-": "-", "": "", "..--..": "?"
    }
    ret = ""

    for i in l:
        if(i == '\n'):
            ret += '  '
        else:
            if i not in morseDict:
                ret += '?'
                continue
            ret += morseDict[i]
    return ret

def _toMorse(l):
    count = 0
    countList = []
    ret = []
    word = ""
    isChar = True

    if(l[0] != 0):
        backIsChar = True
    else:
        backIsChar = False

    for i in l:
        if(0 != i):
            if(not backIsChar):
                countList.append(count)
                count = 0
            backIsChar = True
        else:
            if(backIsChar):
                countList.append(count)
                count = 0
            backIsChar = False
        count += 1

    if(l[0] == 0):
        countList.pop(0)
#    print(countList)   #DEBUG
    dotLen = min(countList)

    for i in countList:
        if(isChar):
            if(i <= dotLen*2):
                word += '.'
            else:
                word += '-'
        else:
            if(dotLen*2 < i <= dotLen*6):
                ret.append(word)
                word = ""
            elif(dotLen*6 < i and word != ""):
                ret.append(word)
                ret.append('\n')
                word = ""
        isChar = not isChar
    ret.append(word)
    return ret

if __name__  == '__main__':
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
        data = rawdata/pow(2,31)
    waveFile.close()

    for i in range(0, len(data), int(N/4*3)):
        if(len(data) < i+N):
            break
        fftData = np.fft.rfft(data[i:i+N]*window)
        ret = np.abs(fftData)/(N/2)

        if(max(ret) > 0.2):
            peak = np.argmax(ret)
            peakList.append(freqList[peak])
        else:
            peakList.append(0)

#print(peakList)    #DEBUG
    morseCode = toMorse(peakList)
#print(morseCode)   #DEBUG
    print(decode(morseCode))
