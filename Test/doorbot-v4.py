import time
import alsaaudio as aa
import pymumble.pymumble_py3 as pymumble
from pymumble.pymumble_py3.constants import *
import audioop
import threading
import subprocess
import wave


class MumbleClient(threading.Thread):
    MUMBLE_CHANNELS = 1 # Mumble hardcoded mono
    MUMBLE_RATE     = 48000 # Mumble hardcoded rate Hz
    MUMBLE_SAMPLESIZE = 2 # Mumble hardcoded bytes per sample    

    ALSA_FORMAT   = aa.PCM_FORMAT_S16_LE # 16 bits litle-endian, must macth mumble sample size
    AUDIO_LEN = 160 # Audio chunk size
    
    def __init__(self):
        self.mumbleUser = "DoorBot"
        self.mumbleHost = "192.168.101.112"
        self.mumblePwd = ""

        self.inputRate = 8000 # Hz
        self.inputDevice = "plughw:1,0"
        self.outputDevice = 0
        self.outputRate = 8000 # Hz

        self.muted = True
        self.deafened = True
        self.digitalVol = 1
        self.silence = 300 # Threshold to detect sound

        try:
            self.input = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, self.inputDevice)
            self.input.setchannels(self.MUMBLE_CHANNELS)
            self.input.setrate(self.inputRate)
            self.input.setformat(self.ALSA_FORMAT)
            self.input.setperiodsize(self.AUDIO_LEN)
        except:
            print("No input device")
        else:
            self.muted = False

        try:
            self.output = aa.PCM(aa.PCM_PLAYBACK, self.outputDevice)
            self.output.setchannels(self.MUMBLE_CHANNELS)
            self.output.setrate(self.outputRate)
            self.output.setformat(self.ALSA_FORMAT)
            self.output.setperiodsize(self.AUDIO_LEN)
        except:
            print("No output device")
        else:
            self.deafened = False

        try:
            self.client = pymumble.Mumble(self.mumbleHost, self.mumbleUser, 64738, self.mumblePwd, None, None, True, [], False)
            self.client.set_codec_profile("audio")
            #self.client.callbacks.set_callback(PYMUMBLE_CLBK_USERCREATED, self.user_created)
            #self.client.callbacks.set_callback(PYMUMBLE_CLBK_USERREMOVED, self.user_removed)
            self.client.callbacks.set_callback(PYMUMBLE_CLBK_SOUNDRECEIVED, self.sound_received)
            self.client.callbacks.set_callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, self.text_received)
            self.client.start()
            self.client.is_ready()
            self.client.set_receive_sound(True)
        except:
            print("No mumble server")
 
        threading.Thread.__init__( self )

    def user_created(self, user):
        return

    def user_removed(self, user, *args):
        return

    def sound_received(self, user, soundchunk):
        user.sound.get_sound() # empty buffer
        if self.deafened != True:
            data, state = audioop.ratecv(soundchunk.pcm, self.MUMBLE_SAMPLESIZE, self.MUMBLE_CHANNELS, self.MUMBLE_RATE, self.outputRate, None)
            self.output.write(data)

    def text_received(self, text):
        msg = text.message.split("=")
        if len(msg) > 0:
            key = msg[0]
            val = ""
            if len(msg) > 1:
                val = msg[1]
            else:
                return
        if key == "hello":
            print("Hello " + val)
        if key == "mute":
            if val == "true": self.muted = True
            else: self.muted = False
            print("Muted " + val)
        if key == "deafen":
            if val == "true": self.deafened = True
            else: self.deafened = False
            print("Deafened " + val)
        if key == "play":
            self.play_wav(val)
        if key == "volume":
            subprocess.call(["amixer", "sset", "PCM", val])
            val = val.replace("%", "")
            if int(val) >= 100:
                self.digitalVol = int(val)/100
            else:
                self.digitalVol = 1
        if key == "silence":
            self.silence = int(val)
   
    def play_wav(self, name):
        d = self.deafened
        self.deafened = True    
        f = wave.open(name, 'rb')
        r = f.getframerate()
        data = f.readframes(320)
        while data:
            data, state = audioop.ratecv(data, self.MUMBLE_SAMPLESIZE, self.MUMBLE_CHANNELS, r, self.outputRate, None)
            self.output.write(data)
            data = f.readframes(320)
        f.close()
        self.deafened = d

    def run(self):
        while True:
            if self.muted != True:
                dataLen, data = self.input.read()
                if dataLen == self.AUDIO_LEN:
                    smin,smax = audioop.minmax(data, self.MUMBLE_SAMPLESIZE)
                    if smax - smin > self.silence:
                        data, state = audioop.ratecv(data, self.MUMBLE_SAMPLESIZE, self.MUMBLE_CHANNELS, self.inputRate, self.MUMBLE_RATE, None)
                        data = audioop.mul(data, self.MUMBLE_CHANNELS, self.digitalVol)
                        self.client.sound_output.add_sound(data)
                        while self.client.sound_output.get_buffer_size() > 0.5:
                            time.sleep(0.01)

if __name__ == '__main__':
    bot = MumbleClient()
    bot.start()
    print("DoorButler running")
    while True:
       time.sleep(0.01)
