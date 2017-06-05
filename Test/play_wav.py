import sys
import wave
import alsaaudio

if __name__ == '__main__':

    device = alsaaudio.PCM(0)
    device.setchannels(1)
    device.setrate(44100)
    device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    device.setperiodsize(320)

    f = wave.open('test.wav', 'rb')

    data = f.readframes(320)
    while data:
        # Read data from stdin
        device.write(data)
        data = f.readframes(320)
       
    f.close()
