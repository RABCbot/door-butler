import time
import alsaaudio as aa
import wave

# constants
MIC_CHANNELS = 1
MIC_FORMAT   = aa.PCM_FORMAT_S16_LE
MIC_RATE     = 8000
MIC_FRAME    = 160

if __name__ == '__main__':

    device = 'plughw:1,0'

    w = wave.open('test.wav', 'w')
    w.setnchannels(MIC_CHANNELS)
    w.setsampwidth(2)
    w.setframerate(MIC_RATE)

    mic = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, device)
    mic.setchannels(MIC_CHANNELS)
    mic.setrate(MIC_RATE)
    mic.setformat(MIC_FORMAT)
    mic.setperiodsize(MIC_FRAME)
    
    while True:
        dataLen, data = mic.read()
        w.writeframes(data)
