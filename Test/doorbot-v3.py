import time
import alsaaudio as aa
import pymumble.pymumble_py3 as pymumble
from pymumble.pymumble_py3.constants import *
import audioop
import threading

class MumbleClient(threading.Thread):
    MUMBLE_CHANNELS = 1 # Mumble hardcoded mono
    MUMBLE_RATE     = 48000 # Mumble hardcoded rate Hz
    MUMBLE_SAMPLESIZE = 2 # Mumble hardcoded bytes per sample    

    ALSA_FORMAT   = aa.PCM_FORMAT_S16_LE # 16 bits litle-endian, must macth mumble sample size
    AUDIO_LEN = 320
    SILENCE  = 256
    
    def __init__(self):
        self.mumbleUser = "DoorBot"
        self.mumbleHost = "192.168.101.112"
        self.mumblePwd = "2putipus"

        self.inputRate = 8000 # Hz
        self.inputDevice = "plughw:1,0"
        self.outputDevice = 0

        self.muted = True
        self.deafened = True

        self.input = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, self.inputDevice)
        self.input.setchannels(self.MUMBLE_CHANNELS)
        self.input.setrate(self.inputRate)
        self.input.setformat(self.ALSA_FORMAT)
        self.input.setperiodsize(self.AUDIO_LEN)

        self.output = aa.PCM(aa.PCM_PLAYBACK, self.outputDevice)
        self.output.setchannels(self.MUMBLE_CHANNELS)
        self.output.setrate(self.MUMBLE_RATE)
        self.output.setformat(self.ALSA_FORMAT)
        self.output.setperiodsize(self.AUDIO_LEN)

        self.client = pymumble.Mumble(self.mumbleHost, self.mumbleUser, 64738, self.mumblePwd, None, None, True, [], False)
        self.client.set_codec_profile("audio")
        self.client.set_receive_sound(True)
        #self.client.callbacks.set_callback(PYMUMBLE_CLBK_USERCREATED, self.user_created)
        #self.client.callbacks.set_callback(PYMUMBLE_CLBK_USERREMOVED, self.user_removed)
        self.client.callbacks.set_callback(PYMUMBLE_CLBK_SOUNDRECEIVED, self.sound_received)
        self.client.start()
        self.client.is_ready()

        threading.Thread.__init__( self )

    def user_created(self, user):
        if self.client.users.count() > 1:
            self.muted = False
        else:
            self.muted = True

    def user_removed(self, user, *args):
        if self.client.users.count() > 1:
            self.muted = False
        else:
            self.muted = True
  
    def sound_received(self, user, soundchunk):
        user.sound.get_sound()
        self.output.write(soundchunk.pcm)

    def run(self):
        while True:
            if self.muted != True:
                dataLen, data = self.input.read()
                if dataLen == self.AUDIO_LEN:
                    smin,smax = audioop.minmax(data, self.MUMBLE_SAMPLESIZE)
                    if smax - smin > self.SILENCE:
                        data, state = audioop.ratecv(data, self.MUMBLE_SAMPLESIZE, self.MUMBLE_CHANNELS, self.inputRate, self.MUMBLE_RATE, None)
                        self.client.sound_output.add_sound(data)
                        while self.client.sound_output.get_buffer_size() > 0.5:
                            time.sleep(0.01)

if __name__ == '__main__':
    bot = MumbleClient()
    bot.start()
    while True:
       time.sleep(1)
