# DoorButler
Smart video doorbell<br/>

## Goal
Device should provide following capabilities
- Smart voice screening (maybe using Alexa, Google or Snips)<br/>
- Video streaming<br/>
- Two way audio<br/>

## Hardware
Raspberry Pi Zero W <http://www.microcenter.com/product/486575/raspberry-pi-zero-w><br/>
Playstation Eye <https://www.amazon.com/Sony-Station-Camera-Packaging-PlayStation-3/dp/B0735KNH2X/ref=pd_lpo_sbs_63_t_1?_encoding=UTF8&psc=1&refRID=TRAC8BQY437JKT9A4417><br/>
Google AIY Voice kit <http://www.microcenter.com/product/483414/aiy-voice-kit><br/>
or Adafruit MAX98357 <https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview><br />

V1:

## Libraries (Credits)
https://github.com/eclipse/paho.mqtt.python<br/>
https://github.com/azlux/pymumble<br/>
https://github.com/larsimmisch/pyalsaaudio<br/>

## Installation
Install motion <http://lavrsen.dk/foswiki/bin/view/Motion/WebHome><br/>
Install mumble-server <http://wiki.mumble.info/wiki/Installing_Mumble><br/>

## Configuration
Find the ALSA recording device:<br/>
arecord -L<br/>

In my case, I get a list of all devices, with the USB Microphone listed as:<br/>
null<br/>
    Discard all samples (playback) or generate zero samples (capture)<br/>
default:CARD=U0x46d0x8ce<br/>
    USB Device 0x46d:0x8ce, USB Audio<br/>
    Default Audio Device<br/>
hw:CARD=U0x46d0x8ce,DEV=0<br/>
    USB Device 0x46d:0x8ce, USB Audio<br/>
    Direct hardware device without any conversions<br/>

Find card index:<br/>
cat /proc/asound/modules<br/>
 0 snd_bcm2835<br/>
 1 snd_usb_audio<br/>

## Test
With the device listed from previous step, perform a quick recording to a file:<br/>
arecord -D plughw:CARD=U0x46d0x8ce,DEV=0 --duration=30 test.wav<br/>

Change volume
amixer sset PCM,0 90%


## Reference
https://bitbucket.org/mkuron/sip2mumble/overview

