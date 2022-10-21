import numpy as np
import wave
from scipy import fftpack, stats
import sys

fname = sys.argv[1]
N = 512
freq = 48000
unitLen = 0
startCharIndex = []

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
"-....-": "-", "": "", "..--..": "?",
"\t": " ", "\n": "\n"
}

binaryList = []

def counter(data):
    count = 5
    countList = []

    noise_count = 5
    start_flag = False
    state = 1
    not_noise_num = 5

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
#                    if state == 1:
#                        startCharIndex.append(i-noise_count-count)
                    state *=-1
                    countList.append(count)
                    count = not_noise_num-1
                    noise_count = 0
    return countList

def getStartCharIndex(data):
    spaceCount = 0
    charLenCount = 0
    lettersList = []
    ret = ""
    tmp = 0
    noise_count = 5
    start_index = 0
    end_index = 0
    start_flag = False
    len_data = len(data)
    i = 0

    while i<len_data:
        if data[i] == -1:
            spaceCount+=1
        if data[i] == 1:
            if unitLen*3 < spaceCount:
                charLenCount = 0
                for j in range(i, i+unitLen):
                    if data[j] == 1:
                        charLenCount+=1
                if unitLen*(4/5) < charLenCount:
                    if unitLen*6 < spaceCount:
                        if unitLen*12 < spaceCount:
                            lettersList.append('\n')
                        else:
                            lettersList.append('\t')
                    lettersList.append(i)
                i+=unitLen
            spaceCount = 0
        i+=1
    '''
    i = 0
    while i<len_data:
        if start_flag == False:
            if data[i] == 1:
                noise_count -= 1
                if noise_count == 0:
                    start_flag = True
            else:
                noise_count = 5
                i += 1
            continue
        else:
            if data[i] == -1:
                i+=1
                continue
            start_index = i
            count = 0
            for j in range(i, len_data):
                if data[j] == 1:
                    count = 0
                    end_index = j
                    continue
                else:
                    count += 1
                    if count >= unitLen/6*5:
                        break
            i = end_index
            if end_index - start_index > 8:
#                lettersList.append([start_index, end_index])
                lettersList.append(start_index)
        i+=1
    '''
    return lettersList

def initBinaryList():
    for morse in morseDict.keys():
        binary = np.full(unitLen*19, -1, dtype='int8')
        index = 0
        for char in morse:
            if char == '.':
                binary[index*unitLen:(index+1)*unitLen] = 1
                index+=2
            if char == '-':
                binary[index*unitLen:(index+3)*unitLen] = 1
                index+=4
        binaryList.append(binary)

def relation_check(data, indexList):
    ret = ""
    morseDictValues = list(morseDict.values())

    for index in indexList:
        ansList = []
        if index == '\t':
            ret += morseDict['\t']
            continue
        if index == '\n':
            ret += morseDict['\n']
            continue
        for binary, value in zip(binaryList, morseDictValues):
            ans = 0
            for i in range(len(binary)):
                ans += data[index+i] * binary[i]
            ansList.append(ans)
        ret += morseDictValues[ansList.index(max(ansList))]
    print(ret)

if __name__ == '__main__':
    window = np.hanning(N)

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

    len_data = len(data)
    tmp = 1.2*pow(10, 15)
    fftFreq = 64
    peakList = np.full(int(len_data/fftFreq+1), -1, dtype="int8")

    for i in range(0, len_data, fftFreq):
        if(len_data-i < N):
            break
        fftData = np.fft.rfft(data[i:i+N]*window)
        ret = np.abs(fftData)/(N/2)
        var = np.var(ret, ddof=0)

        if(var > tmp):
            peakList[int(i/fftFreq)] = 1

    countList = counter(peakList)
    median = round(np.median(countList))
    unitLen = round(stats.tmean(countList, (median-5, median+5)))-1
    print(unitLen)
    initBinaryList()
    startCharIndex = getStartCharIndex(peakList)
    print(startCharIndex)
    relation_check(peakList, startCharIndex)
