import time
import alsaaudio as aa
import pymumble.pymumble_py3 as pymumble
import audioop

# constants
MIC_CHANNELS  = 1 # mono
MIC_FORMAT    = aa.PCM_FORMAT_S16_LE # 16 bits litle-endian
MIC_DEPTH     = 2 # two bytes per sample
MIC_RATE      = 8000 # Hz
MIC_FRAMESIZE = 1600 # 20 ms
MIC_DEVICE    = 'plughw:1,0' 
MUMBLE_PACKETLEN = 0.02 # 20 ms
MUMBLE_RATE   = 48000 # Hz

def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a

if __name__ == '__main__':

    # Init Alsa Microphone
    mic = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, MIC_DEVICE)
    mic.setchannels(MIC_CHANNELS)
    mic.setrate(MIC_RATE)
    mic.setformat(MIC_FORMAT)
    mic.setperiodsize(MIC_FRAMESIZE)

    # Init Mumble client
    client = pymumble.Mumble('192.168.101.112', 'DoorBot', 64738, '2putipus', None, None, True, [], False)
    client.set_codec_profile('audio')
    client.start()
    client.is_ready()
    client.set_receive_sound(True)
    client.sound_output.set_audio_per_packet(MUMBLE_PACKETLEN)

    sound = ''
    while True:
        dataLen, data = mic.read()
        while dataLen:
            sound = list(data)
            sound = audioop.ratecv(sound, MIC_DEPTH, MIC_CHANNELS, MIC_RATE, MUMBLE_RATE, None)
            client.sound_output.add_sound(sound)
            while client.sound_output.get_buffer_size() > 0.5:
                time.sleep(0.01)

