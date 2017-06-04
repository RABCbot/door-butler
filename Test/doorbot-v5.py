import time
import alsaaudio as aa
import pymumble.pymumble_py3 as pymumble
from pymumble.pymumble_py3.constants import *
import audioop
from threading import Thread
import queue
import subprocess
import wave

AUDIO_LEN         = 160 # Audio chunk size
MUMBLE_CHANNELS   = 1 # Mumble hardcoded mono
MUMBLE_RATE       = 48000 # Mumble hardcoded rate Hz
MUMBLE_SAMPLESIZE = 2 # Mumble hardcoded bytes per sample
ALSA_FORMAT       = aa.PCM_FORMAT_S16_LE # 16 bits litle-endian, must macth mumble sample size

captureQueue = queue.Queue()
playQueue = queue.Queue()
 
class MumbleBot(Thread):
    
    def __init__(self, host, usr, pwd, rate):
        self.mumbleHost = host
        self.mumbleUsr = usr
        self.mumblePwd = pwd
        self.rate = rate
        self.volume = 1

        try:
            self.client = pymumble.Mumble(self.mumbleHost, self.mumbleUsr, 64738, self.mumblePwd, None, None, True, [], False)
            self.client.set_codec_profile("audio")
            #self.client.set_loop_rate(0.01)
            #self.client.callbacks.set_callback(PYMUMBLE_CLBK_USERCREATED, self.user_created)
            #self.client.callbacks.set_callback(PYMUMBLE_CLBK_USERREMOVED, self.user_removed)
            self.client.callbacks.set_callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, self.text_received)
            self.client.start()
            self.client.is_ready()
        except:
            print("Unable to initialize mumble client")

        Thread.__init__( self )
 
    def user_created(self, user):
        return

    def user_removed(self, user, *args):
        return

    def text_received(self, text):
        msg = text.message.split(" ")
        if len(msg) > 0:
            key = msg[0]
            val = ""
            if key == "hello": print("Hello World!")
            if len(msg) > 1:
                val = msg[1]
            else:
                return

    def run(self):
        while True:
            data = captureQueue.get()
            data, state = audioop.ratecv(data, MUMBLE_SAMPLESIZE, MUMBLE_CHANNELS, self.rate, MUMBLE_RATE, None)
            # data = audioop.mul(data, self.MUMBLE_CHANNELS, self.digitalVol)
            # self.client.sound_output.add_sound(data)
            # captureQueue.task_done()
            time.sleep(0.02)
            # while self.client.sound_output.get_buffer_size() > 0.5: time.sleep(0.01)
                
class PlayAudio(Thread):
    
    def __init__(self, device, rate):
        self.deafened = True
        self.rate = rate

        try:
            self.output = aa.PCM(aa.PCM_PLAYBACK, self.outputDevice)
            self.output.setchannels(mumble.MUMBLE_CHANNELS)
            self.output.setrate(self.outputRate)
            self.output.setformat(mumble.ALSA_FORMAT)
            self.output.setperiodsize(mumble.AUDIO_LEN)
        except:
            print("Unable to initialize output audio")
        else:
            self.deafened = False

 
        Thread.__init__( self )

    def run(self):
        while True:
            if self.deafened != True:
                data = playQueue.get()
                data, state = audioop.ratecv(data, MUMBLE_SAMPLESIZE, MUMBLE_CHANNELS, MUMBLE_RATE, self.rate, None)
                self.output.write(data)
                playQueue.task_done()
                time.sleep(0.05)

class CaptureAudio(Thread):
    
    def __init__(self, device, rate):
        self.silence = 300 # Threshold to detect sound
        self.muted = True

        try:
            self.input = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, device)
            self.input.setchannels(MUMBLE_CHANNELS)
            self.input.setrate(rate)
            self.input.setformat(ALSA_FORMAT)
            self.input.setperiodsize(AUDIO_LEN)
        except:
            print("Unable to initialize input audio")
        else:
            self.muted = False

#        self.wav = wave.open('tone.wav', 'rb')

        Thread.__init__( self )

    def run(self):
        i = 0
        while True:
            if self.muted != True:
                dataLen, data = self.input.read()
                #dataLen = AUDIO_LEN
                #data = self.wav.readframes(AUDIO_LEN)
                if dataLen == AUDIO_LEN:
                    smin,smax = audioop.minmax(data, MUMBLE_SAMPLESIZE)
                    if smax - smin > self.silence:
                        captureQueue.put(data)
                        #captureQueue.join()


if __name__ == '__main__':

    rate = 8000
    bot = MumbleBot("192.168.101.112", "DoorBot", "", rate)
    bot.setDaemon(True)
    bot.start()

    mic = CaptureAudio("plughw:1,0", rate)
    mic.setDaemon(True)
    mic.start()

#    spk = PlayAudio(0, 8000)
#    spk.setDaemon(True)
#    spk.start()

    print("DoorBot running...")
    while True: time.sleep(1)

