import wave
from scipy.io import wavfile
import numpy as np
import math
import python_speech_features.base as mfcc 


def get_data_from_file(filename):
    print(filename)   
    fs, data = wavfile.read(filename)
    
    if(data.ndim >= 2):
        new_data = data[:,0]
    else:
        new_data = data  
    print("HEY LOOK AT HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1",len(new_data))
    return  new_data

def cut(arr,filename):
    with wave.open(filename, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
    ave = sum(arr)/len(arr)
    ave = ave/10
    b = []
    index = False
    for i in range(len(arr)):
        if(abs(arr[i]) <= abs(ave) and index == False):
            continue
        elif(abs(arr[i]) >= abs(ave) and index == False):
            index = True
            b.append(arr[i])
        elif(abs(arr[i]) <= abs(ave) and index == True):
            b.append(arr[i])
        elif(abs(arr[i]) >= abs(ave) and index == True):
            b.append(arr[i])
    #print(b)
    print("//////////////////////////////////////////////*********************************//////////////////////////////////////////////////////////")
    index = False
    #print(ave)
    c = []
    for i in range(len(b)):
        if(abs(b[len(b) - i - 1]) <= abs(ave) and index == False):
            continue
        elif(abs(b[len(b) - i - 1]) >= abs(ave) and index == False):
            index = True
            c.insert(0,b[len(b) - i - 1])
        elif(abs(b[len(b) - i - 1]) <= abs(ave) and index == True):
            c.insert(0,b[len(b) - i - 1])
        elif(abs(b[len(b) - i - 1]) >= abs(ave) and index == True):
            c.insert(0,b[len(b) - i - 1])
    #print(c)
    c = np.array(c)
    cuted_filename = filename + "1" +".wav"
    wavfile.write(cuted_filename,frame_rate,c)
    return (c, cuted_filename)

def get_mfcc(signal, filename):
    with wave.open(filename, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
    sig_mfcc = mfcc.mfcc(signal,frame_rate,)
    #print(sig_mfcc)
    return sig_mfcc

def stretch( fname,  factor ):
    infile=wave.open( fname, 'rb')
    rate= infile.getframerate()
    channels=infile.getnchannels()
    swidth=infile.getsampwidth()
    nframes= infile.getnframes()
    audio_signal= infile.readframes(nframes)
    stretched = fname + "str.wav"
    #print(stretched)
    outfile = wave.open(stretched, 'wb')
    outfile.setnchannels(channels)
    outfile.setsampwidth(swidth)
    outfile.setframerate(rate/factor)
    outfile.writeframes(audio_signal)
    outfile.close()
    return stretched


def stretch_files(et , sig, sig_filename):
    el = len(et)
    sil = len(sig)
    factor_kot = el/sil
    factor = factor_kot
# =============================================================================
#     if((factor_kot - math.floor(factor_kot)) < 0.5):
#         factor = math.floor(factor_kot) + 0.5
# =============================================================================
    print("write down the factor!",factor)
    new = stretch( sig_filename, factor )
    return new


def remove_deltas(et ,sig):
    new_sig = []
    new_sig_elem = []
    ave_K = 0
    N = 0
    ave_K_1 = []
    ave_K_2 = []
    print(len(et))
    print(len(sig))
    for m in range(len(et)):
        for j in range(len(et[m])):
            ave_K_1.append(math.pow((et[m][j] - sig[m][j]),2))
            ave_K_2.append(math.pow(et[m][j],2) - math.pow(sig[m][j],2))
            N = len(et[m])
        ave_K = math.sqrt((sum(ave_K_1)/(N) - sum(ave_K_2)/(N)))
        #print(ave_K)
        for j in range(len(sig[m])):
            new_sig_elem.append(sig[m][j] - ave_K)
            
        new_sig.append(new_sig_elem)
        new_sig_elem = []
    return new_sig


def compare(et , sig):
    per_elem = []
    percents = []
    per = 0
    for i in range(len(et)):
        for j in range(len(et[i])):
            x = math.sqrt((math.pow((et[i][j] - sig[i][j]),2))/(abs(et[i][j]) + 0.001))
            #print(x)
            if(x > 100):
                x = 100
            #print(x)
            per_elem.append(100 - x)
        percents.append(sum(per_elem)/len(per_elem))
    #print(percents)
    per = sum(percents)/len(percents)
    print(per)
    return per
    
    
def main(f1,f2):
    a = get_data_from_file(f1)
    b = get_data_from_file(f2)
    
    
    stretched = stretch_files(a, b, f2)
    b = get_data_from_file(stretched)
    b_mfcc = get_mfcc(b, stretched)
    a_mfcc = get_mfcc(a, f1)
    b_mfcc = remove_deltas(a_mfcc, b_mfcc)
    compare(a_mfcc, b_mfcc)

main("07.wav", "07.wav")










