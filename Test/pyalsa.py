import sys
import time
import getopt
import alsaaudio as aa
import audioop

# constants
MIC_CHANNELS = 1
MIC_FORMAT   = aa.PCM_FORMAT_S16_LE
MIC_RATE     = 8000
MIC_FRAME    = 512
MIC_DEVICE = 'plughw:1,0'

if __name__ == '__main__':

    mic = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, MIC_DEVICE)
    mic.setchannels(MIC_CHANNELS)
    mic.setrate(MIC_RATE)
    mic.setformat(MIC_FORMAT)
    mic.setperiodsize(MIC_FRAME)

    f = open('test.raw', 'wb')
  
    while True:
        l, data = mic.read()
        sound, state = audioop.ratecv(data, 2, 1, 8000, 48000, None)
        f.write(sound)
