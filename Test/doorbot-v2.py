import time
import alsaaudio as aa
import pymumble.pymumble_py3 as pymumble
import audioop

# constants
MIC_CHANNELS    = 1 # mono
MIC_FORMAT      = aa.PCM_FORMAT_S16_LE # 16 bits litle-endian
MIC_SAMPLESIZE  = 2 # two bytes per sample
MIC_RATE        = 8000 # Hz
MIC_PERIOD      = 160 # 20 ms
MIC_DEVICE      = "plughw:1,0"
MIC_SILENCE     = 1024


MUMBLE_HOST = "192.168.101.112"
MUMBLE_CLIENTNAME = "DoorBot"
MUMBLE_PASSWORD = "password"
MUMBLE_PACKETLEN = 0.02 # 20 ms
MUMBLE_RATE   = 48000 # Hz

if __name__ == "__main__":

    # Init Alsa Microphone
    mic = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, MIC_DEVICE)
    mic.setchannels(MIC_CHANNELS)
    mic.setrate(MIC_RATE)
    mic.setformat(MIC_FORMAT)
    mic.setperiodsize(MIC_PERIOD)

    # Init Mumble client
    client = pymumble.Mumble(MUMBLE_HOST, MUMBLE_CLIENTNAME, 64738, MUMBLE_PASSWORD, None, None, True, [], False)
    client.set_codec_profile("audio")
    client.start()
    client.is_ready()
    client.set_receive_sound(True)
    client.users.myself.unmute()
#    client.sound_output.set_audio_per_packet(MUMBLE_PACKETLEN)

    while True:
        dataLen, data = mic.read()
        if dataLen == MIC_PERIOD:
            smin,smax = audioop.minmax(data, MIC_SAMPLESIZE)
            if smax - smin > MIC_SILENCE:
                sound, state = audioop.ratecv(data, MIC_SAMPLESIZE, MIC_CHANNELS, MIC_RATE, MUMBLE_RATE, None)
                client.sound_output.add_sound(sound)
                while client.sound_output.get_buffer_size() > 0.5:
                    time.sleep(0.01)

